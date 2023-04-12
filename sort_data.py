import json, copy, sys, time, csv
import numpy as np
import datetime
import matplotlib.pyplot as plt

# two data sets - first is in UTC
file = open('outage_data.json')
input_data = json.load(file)
data = {}
timesteps = []
        
for k in input_data:
    y = int(k[:4])
    m = int(k[5:7])
    d = int(k[8:10])
    h = int(k[11:13])
    mi = int(k[14:16])
    dt = datetime.datetime(y,m,d,h,mi)
    data[dt] = input_data[k]
    timesteps.append(dt)
    
# second is in local CO time
timesteps = sorted(timesteps)
# find the length of each timestep
file = open('outage_data_2.json')
input_data2 = json.load(file)
        
for k in input_data2:
    y = int(k[:4])
    m = int(k[5:7])
    d = int(k[8:10])
    h = int(k[11:13])
    mi = int(k[14:16])
    dt = datetime.datetime(y,m,d,h,mi)
    
    # but need to convert to UTC
    if dt <= datetime.datetime(2022,11,6,2): # daylight savings
        dt += datetime.timedelta(hours=6)
    elif dt <= datetime.datetime(2023,3,2,2): # before daylight savings
        dt += datetime.timedelta(hours=7)
    elif dt <= datetime.datetime(2023,11,5,2): # daylight savings
        dt += datetime.timedelta(hours=6)
    data[dt] = input_data2[k]
    timesteps.append(dt)

ts_l = {}
t = 0
while t < len(timesteps)-1:
    ts_l[timesteps[t]] = round((timesteps[t+1]-timesteps[t]).seconds/3600,2)
    t += 1
ts_l[timesteps[t]] = round(1/12,2)# assume 5 mins

# first let's make a list for each zip code of the outages
zips = {}
for ts in timesteps:
    for z in data[ts]:
        if z not in zips:
            zips[z] = []
        zips[z].append([ts,data[ts][z]])

events = []
for z in zips:
    start = zips[z][0][0]
    end = start + datetime.timedelta(seconds=int(3600*ts_l[zips[z][0][0]]))
    total = zips[z][0][1]*ts_l[zips[z][0][0]]
    for i in range(1,len(zips[z])):
        if (zips[z][i][0]-zips[z][i-1][0]).seconds < 10*60:
            total += zips[z][i][1]*ts_l[zips[z][i][0]]
            end += datetime.timedelta(seconds=int(3600*ts_l[zips[z][0][0]]))
        else:
            if total > 0:
                events.append([start,end,z,total])
            start = zips[z][i][0]
            total = zips[z][i][1]*ts_l[zips[z][i][0]]
            end = start + datetime.timedelta(seconds=int(3600*ts_l[zips[z][0][0]]))
    if total > 0:
        events.append([start,end,z,total])

        
events = sorted(events)
with open('Outage Events.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Start (UTC)','End (UTC)','Zip Code','Customer-hrs'])
    writer.writerows(events)
    

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
        