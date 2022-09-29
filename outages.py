import requests
import time
import datetime

def scrape():
    x = requests.get('https://xcelenergy-ags.esriemcs.com/arcgis/rest/services/XcelOutage/MapServer/4/query?f=json&where=1%3D1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=ZIPCODE%2CTOTALCUSTOMERS%2CCUSTOMERSOUT&orderByFields=&cacheBuster=1664457753959')

    r = x.text

    data = []

    i = 0
    while i < len(r)-10:
        while r[i:i+11] != '{"ZIPCODE":':
            i += 1
        i += 1
        j = i+1
        while r[j:j+2] != '}}':
            j += 1
        data.append(r[i:j])
        i = j

    d = datetime.datetime.now()
    name = str(d.year)+'_'+str(d.month)+'_'+str(d.day)+'_'+str(d.hour)+'_'+str(d.minute)+'.txt'
    print(name)
    f = open('outage_data/'+name,'w')
    for i in range(1,len(data)):
        f.write(data[i]+'\n')
    f.close()

scrape()
#while True:
#    scrape()
#    time.sleep(300)
    