# Creates a table from a versionized csv file

import csv
import sys
from distutils.version import StrictVersion

table = {}
rows = set() 

with open('out.csv') as csvfile:
    reader = csv.reader(csvfile);
    for y,x,f in reader:
        rows.add(x)
        table.setdefault(x, {"name": x})[y] = f

versions = sorted(rows, key=StrictVersion)
writer = csv.DictWriter(
    sys.stdout, 
    fieldnames=["name"] + versions
)
writer.writeheader()
for rowid in versions:
    writer.writerow(table[rowid])

