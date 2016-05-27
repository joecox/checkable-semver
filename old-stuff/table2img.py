
from PIL import Image
from itertools import product
import csv
import sys

table = {}
versions = []
with open(sys.argv[1]) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader: 
        versions.append(row["name"])
        table[row["name"]] = row

size = len(versions)
img = Image.new("L", (size, size))
data = [int(table[tid][iid]) for tid, iid in product(versions, repeat=2)]
img.putdata(data, 255, 128)
img.save(sys.argv[1].rsplit(".", 1)[0] + ".png")


