import json, copy, sys, time, csv, requests

r = requests.get('https://developer.nrel.gov/api/solar/nsrdb_data_query.json?api_key=0OQbvRZEWNfZGU6KJwLPYKjhbCk6gXbf9QNS0RGY&lat=39.973222&lon=-105.209276&names=2021')
data = r.json()

for d in data['outputs']:
    print(d['name'])
    for l in d['links']:
        print(l['year'])