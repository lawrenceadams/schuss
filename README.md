# schuss
Schuss - Command line status for the Gstaad ski-resort lift operation.

Able to get lifts in operation at present at Gstaad (as of May 2021)

## Operation
Simply call the file for an automatic result:

`$ python3 ./schuss.py`

Alternatively, specify an `-w` or `-s` flag for winter or summer results respectively:

```
$ python3 ./schuss.py -h
usage: schuss.py [OPTION]

Print Gstaad Ski Lift status at present. Defaults to mode appropriate for time
of year.

optional arguments:
  -h, --help     show this help message and exit
  -w, --winter   Use summer mode
  -s, --summer   Use winter mode
  -v, --version  show program's version number and exit
```

https://user-images.githubusercontent.com/4786533/118476876-f77fcf00-b705-11eb-9d12-e1e3bf6f788f.mov

