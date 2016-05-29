# Creates a table from a versionized csv file

import csv
import sys

from distutils.version import StrictVersion
from itertools import product

table = {}
rows = set() 

reader = csv.reader(sys.stdin);
for y,x,f in reader:
    rows.add(y)
    table.setdefault(x, {"name": x})[y] = f

versions = sorted(rows, key=StrictVersion)

for name, version in product(versions, repeat=2):
    table.setdefault(name, {"name": name}).setdefault(version, "-1")

writer = csv.DictWriter(
    sys.stdout, 
    fieldnames=["name"] + versions
)
writer.writeheader()
for rowid in versions:
    writer.writerow(table[rowid])

