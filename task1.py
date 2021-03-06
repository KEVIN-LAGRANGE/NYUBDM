# -*- coding: utf-8 -*-
"""Untitled3.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1BZ-nUQWdliZPwFSwdtijhjCfd7hNOkR3
"""

# -*- coding: utf-8 -*-
"""Untitled2.ipynb
Automatically generated by Colaboratory.
Original file is located at
    https://colab.research.google.com/drive/1E1nrwuxgxGDNYdnyz2yAFEjdvFPVts_S
"""

# Commented out IPython magic to ensure Python compatibility.

import csv
import json
import numpy as np


import pandas as pd



import pyspark
from pyspark import SparkContext
import sys
from pyspark.sql import SparkSession


data = pd.read_csv('keyfood_sample_items.csv')
l = []
for i in data["UPC code"]:
    l.append(i.split('-')[1])
data["UPC code"]=l
l1 = []
for i in data["Item Name"]:
    
    l1.append(i)
t1 = pd.Series(l1, index=l)
json_data = pd.read_json("keyfood_nyc_stores.json",orient = "columns")
json_data = pd.DataFrame(json_data.values.T, index=json_data.columns, columns=json_data.index)
Insecurity = json_data["foodInsecurity"]
def extractSchools(partId, part):
    if partId==0:
        next(part)
    import csv
    for record in csv.reader(part):
      a = record[2].split('-')[-1]
      if int(record[0]) in list(Insecurity.index) and a in l:
        yield (t1[a], float(record[5][1:5]),int(100*Insecurity[int(record[0])]))



if __name__=='__main__':
  
  sc = SparkContext()
  sc.textFile('/tmp/bdm/keyfood_products.csv', use_unicode=True) \
        .mapPartitionsWithIndex(extractSchools) \
        .saveAsTextFile('output')
