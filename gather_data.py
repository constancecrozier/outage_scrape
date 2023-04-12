import requests
import time
import datetime
import csv
import os
import matplotlib.pyplot as plt
import numpy as np
import json

# replace this with a list of files from the directory
files = sorted(os.listdir('outage_data'))
totals = {}
totals_n = {}
instances = {}
n_t = 0

data = {}
logs = {}
daily = {'8':{},'5':{}}
dmin = datetime.datetime(2025,1,1)
dmax = datetime.datetime(2020,1,1)
for file in files:
    y = int(file[:4])
    i = 5
    j = i
    while file[j] != '_':
        j += 1
    m = int(file[i:j])
    i = j+1
    j = i
    while file[j] != '_':
        j += 1
    d = int(file[i:j])
    i = j+1
    j = i
    while file[j] != '_':
        j += 1
    h = int(file[i:j])
    i = j+1
    j = i
    while file[j] != '.':
        j += 1
    mi = int(file[i:j])
    
    dt = datetime.datetime(y,m,d,h,mi)
    dt = str(dt)
    data[dt] = {}
    with open('outage_data/'+file,'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            i = 0
            while row[0][i] != ':':
                i += 1
            try:
                zipcode = int(row[0][i+2:-1])
            except:
                continue
            i = 0
            while row[1][i] != ':':
                i += 1
            n_t = int(float(row[1][i+1:]))
            i = 0
            while row[2][i] != ':':
                i += 1
            n = int(float(row[2][i+1:]))
            data[dt][zipcode] = n


json_object = json.dumps(data, indent=2)
with open('outage_data.json', "w") as outfile:
    outfile.write(json_object)

        
        
        

            