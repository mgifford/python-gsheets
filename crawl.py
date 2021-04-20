#!/usr/bin/env python

# Pull in libraries
import gspread
import csv

from simplified_scrapy import req, SimplifiedDoc
url = 'https://www.census.gov/'
html = req.get(url)
doc  = SimplifiedDoc(html)
lstA = doc.listA(url=url) # This is the result of de duplication
csvRow = [a.url for a in lstA]
# print(csvRow)

for row in csv.reader(csvRow):
    if row.startswith("[") and row.endswith("]"):
      row = string[1:-1]
    print (row)

# with "a" as fp
#  print(fp)
#  print(csvRow)

# csvfile = "urls1.csv"
# with open(csvfile, "a") as fp:
#   wr = csv.writer(fp, dialect='excel')
#  wr.writerow(csvRow )
