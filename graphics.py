import json, copy, sys, time, csv
import numpy as np
import datetime
import matplotlib.pyplot as plt

zips = []
events = []
with open('Outage Events.csv','r') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        k = row[0]
        y = int(k[:4])
        m = int(k[5:7])
        d = int(k[8:10])
        h = int(k[11:13])
        mi = int(k[14:16])
        start = datetime.datetime(y,m,d,h,mi)
        k = row[1]
        y = int(k[:4])
        m = int(k[5:7])
        d = int(k[8:10])
        h = int(k[11:13])
        mi = int(k[14:16])
        end = datetime.datetime(y,m,d,h,mi)
        z = row[2]
        if z not in zips:
            zips.append(z)
        chours = float(row[3])
        events.append([start,end,z,chours])

d0 = datetime.datetime(2022,9,29,14,20)
co = np.zeros((35,))
mn = np.zeros((35,))
for i in range(len(events)):
    w = int((events[i][0]-d0).days/7)
    if events[i][2][0] == '8':
        co[w] += events[i][3]
    elif events[i][2][0] == '5':
        mn[w] += events[i][3]

plt.figure()
plt.bar(range(35),co+mn)
plt.bar(range(35),co)
plt.show()
        
x = []
y = []

x2 = []
y2 = []

for i in range(len(events)):
    if events[i][2][0] == '8':
        x.append(events[i][0])
        y.append(events[i][3])
    else:
        x2.append(events[i][0])
        y2.append(events[i][3])
    
plt.figure()
plt.scatter(x,y)
plt.scatter(x2,y2)
plt.show()
        