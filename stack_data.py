import requests
import time
import datetime
import csv
import os
import matplotlib.pyplot as plt
import numpy as np

# replace this with a list of files from the directory
files = sorted(os.listdir('outage_data'))
totals = {}
totals_n = {}
instances = {}
n_t = 0

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
    d_ = datetime.datetime(y,m,d)
    if d_ not in daily['5']:
        daily['5'][d_] = 0
        daily['8'][d_] = 0
    if d_ < dmin:
        dmin = d_
    if d_ > dmax:
        dmax = d_
    n_t += 1
    for zipcode in logs:
        logs[zipcode][dt] = 0
    # convert file name to timestamp here if I want
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
            if zipcode not in totals:
                totals[zipcode] = 0
                totals_n[zipcode] = 0
                instances[zipcode] = 0
                logs[zipcode] = {}
            totals[zipcode] += n*0.3
            totals_n[zipcode] += n*0.3/n_t
            instances[zipcode] += 1
            logs[zipcode][dt] = 1
            if int(zipcode/10000) == 5:
                daily['5'][d_] += n*0.3
            else:
                daily['8'][d_] += n*0.3

x = []
y1 = []
y2 = []
d = dmin
while d <= dmax:
    x.append(d)
    try:
        y1.append(daily['5'][d])
    except:
        y1.append(0)
    try:
        y2.append(daily['8'][d])
    except:
        y2.append(0)
    d += datetime.timedelta(1)
y1 = np.array(y1)
y2 = np.array(y2)

plt.figure()
plt.bar(x,y1+y2,label='CO',zorder=2)
plt.bar(x,y1,label='MN',zorder=3)
plt.ylabel('Customer Hours')
plt.xlabel('Day')
plt.grid(zorder=1)
plt.legend()
plt.tight_layout()
plt.show()
with open('sum.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Zipcode','Customer-Hours','Av time per customer (hrs)','% with issues'])
    for z in totals:
        writer.writerow([z,totals[z],totals_n[z],instances[z]*100/n_t])
            
            
# Now to calculate duration of the outages
av_dur = {}
for zipcode in logs:
    dur = []
    timesteps = sorted(list(logs[zipcode].keys()))
    out = False
    nt = 0
    for dt in timesteps:
        if logs[zipcode][dt] == 0:
            if out == False:
                continue
            else:
                dur.append(nt)
                out = False
                nt = 0
        if logs[zipcode][dt] == 1:
            out = True
            nt += 1
    av_dur[zipcode] = sum(dur)/len(dur)
    
with open('len.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Zipcode','Average Resolution (5m)'])
    for z in av_dur:
        writer.writerow([z,av_dur[z]])
        
        
        
        

            