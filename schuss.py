import urllib.request
from bs4 import BeautifulSoup

# Gstaad status API end point
STATUS_API_URL = "https://www.infosnow.ch/~apgmontagne/?lang=en&id=39&tab=web-su"

OPEN_STRING =        "    OPEN    ✅"
PREPERATION_STRING = "PREPERATION ⏳"
CLOSED_STRING =      "   CLOSED   ⛔️"

# Try to open status URL, and handle any errors
print("Contacting server...", end='', flush=True)
try:
    with urllib.request.urlopen(STATUS_API_URL) as request:
        o = request.read()
    print("OK")

# Catch URL errors (e.g. service down/disconnected)
except urllib.request.URLError as e:
    print("Failed to connect to status server.")
    print(e.reason)

# Get status of services
soup = BeautifulSoup(o, "html.parser")

lifts_block = soup.find_all("td", {"class": "cell3"})

lift_dict = {}

divs = soup.find_all("div", {"class": "content"})[1:3]

# for div in divs:
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
