#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Python script to fetch/scrape data from infosnow.ch to see what lifts are open at Gstaad at present.
Can be run in Summer or Winter mode (defaults to time of year).
"""

__version__ = "0.0.4"
__author__ = "Lawrence Adams"

import argparse
import datetime
import sys
import urllib.request
from bs4 import BeautifulSoup

# Gstaad status API end point
STATUS_API_URL_WINTER = "https://www.infosnow.ch/~apgmontagne/?lang=en&id=39&tab=web-wi"
STATUS_API_URL_SUMMER = "http://www.infosnow.ch/~apgmontagne/?lang=en&pid=39&tab=web-su"

OPEN_STRING =        "    OPEN    ✅"
PREPERATION_STRING = "PREPERATION ⏳"
CLOSED_STRING =      "   CLOSED   ⛔️"


def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="%(prog)s [OPTION]",
        description="Print Gstaad Ski Lift status at present. Defaults to mode appropriate for time of year."
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-w", "--winter", action="store_true",
        help="Use summer mode"
    )
    group.add_argument(
        "-s", "--summer", action="store_true",
        help="Use winter mode"
    )
    parser.add_argument(
        "-v", "--version", action="version",
        version=f"{parser.prog} version {__version__}"
    )
    return parser

def main() -> str:
    """
    Parse command line arguments. If none given, detect month and use appropriate mode.
    :return URL string for winter/summer mode
    """
    parser = init_argparse()
    args = parser.parse_args()

    if args.winter:
        return STATUS_API_URL_WINTER
    elif args.summer:
        return  STATUS_API_URL_SUMMER
    else:
        dt = datetime.date.today().month
        if dt == 12 or dt < 5:
            print("[Auto] Winter 🌨")
            return STATUS_API_URL_WINTER
        else:
            print("[Auto] Summer 🌞")
            return STATUS_API_URL_SUMMER
        
STATUS_API_URL = main()

# Try to open status URL, and handle any errors
print("Contacting server...", end='', flush=True)
try:
    with urllib.request.urlopen(STATUS_API_URL) as request:
        o = request.read()
    print("OK")

# Catch URL errors (e.g. service down/disconnected)
except urllib.request.URLError as e:
    print(" Error!")
    print("Failed to connect to status server. Check internet connection.")
    print(e.reason)
    sys.exit(1) # Exit in error state

# Get status of services
soup = BeautifulSoup(o, "html.parser")

lifts_block = soup.find_all("td", {"class": "cell3"})

# Check len is sufficient; else raise error
if len(lifts_block) == 0:
    print("Unable to scrape site: no values returned. Site setup may have changed.\n Please contact maintainer.")
    raise RuntimeError("[Error] Scraped content length == 0")


lift_dict = {}

divs = soup.find_all("div", {"class": "content"})

def get_lift_data(input_divs, output_dict):
    for td in input_divs.find_all("td", {"class": "cell3"}):
        for tr in td.find_all("tr"):
            lift_name = str(tr.find("td", {"class": "txtBox3"}).encode_contents(), 'utf-8').strip()

            lifts_status = tr.find_all("img")
            for lift in lifts_status:
                if lift['src'] == "//www.infosnow.ch/~apgmontagne/data/status/8/1.gif":
                    output_dict[lift_name] = OPEN_STRING
                elif lift['src'] == "//www.infosnow.ch/~apgmontagne/data/status/8/2.gif":
                    output_dict[lift_name] = PREPERATION_STRING
                elif lift['src'] == "//www.infosnow.ch/~apgmontagne/data/status/8/3.gif":
                    output_dict[lift_name] = CLOSED_STRING
                else:
                    pass # Ignore lift icons at present
    return output_dict

for div in divs:
    get_lift_data(div, lift_dict)


print("======= LIFTS =======")
for lift in lift_dict:
    print(f"{lift_dict[lift]} {lift}")
