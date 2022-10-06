import requests
import time
import datetime
import csv

# replace this with a list of files from the directory
files = ['2022_9_29_18_23.txt','2022_9_29_18_51.txt','2022_9_29_19_9.txt','2022_9_29_19_29.txt','2022_9_29_19_41.txt','2022_9_29_19_55.txt','2022_9_29_20_24.txt','2022_9_29_20_48.txt','2022_9_29_21_0.txt','2022_9_29_21_28.txt','2022_9_29_21_49.txt','2022_9_29_22_6.txt','2022_9_29_22_35.txt','2022_9_29_22_53.txt','2022_9_29_23_22.txt','2022_9_29_23_52.txt','2022_9_30_1_27.txt','2022_9_30_4_18.txt','2022_9_30_5_49.txt','2022_9_30_6_42.txt','2022_9_30_7_28.txt','2022_9_30_8_1.txt','2022_9_30_8_47.txt','2022_9_30_9_15.txt','2022_9_30_9_46.txt','2022_9_30_10_1.txt','2022_9_30_10_35.txt','2022_9_30_10_54.txt','2022_9_30_11_16.txt','2022_9_30_11_38.txt','2022_9_30_11_51.txt','2022_9_30_12_21.txt','2022_9_30_13_26.txt','2022_9_30_14_18.txt','2022_9_30_14_51.txt','2022_9_30_15_15.txt','2022_9_30_15_46.txt','2022_9_30_16_10.txt','2022_9_30_16_59.txt','2022_9_30_17_42.txt','2022_9_30_18_2.txt','2022_9_30_18_41.txt','2022_9_30_19_3.txt','2022_9_30_19_29.txt','2022_9_30_19_45.txt','2022_9_30_19_56.txt','2022_9_30_20_27.txt','2022_9_30_20_49.txt','2022_9_30_21_0.txt','2022_9_30_21_28.txt','2022_9_30_21_47.txt','2022_9_30_21_58.txt','2022_9_30_22_30.txt','2022_9_30_22_51.txt','2022_9_30_23_12.txt','2022_9_30_23_43.txt','2022_10_1_0_2.txt','2022_10_1_3_16.txt','2022_10_1_5_0.txt','2022_10_1_6_6.txt','2022_10_1_6_50.txt','2022_10_1_7_16.txt','2022_10_1_7_42.txt','2022_10_1_7_55.txt','2022_10_1_8_27.txt','2022_10_1_8_56.txt','2022_10_1_9_26.txt','2022_10_1_9_48.txt','2022_10_1_9_59.txt','2022_10_1_10_31.txt','2022_10_1_10_52.txt','2022_10_1_11_10.txt','2022_10_1_11_32.txt','2022_10_1_11_46.txt','2022_10_1_11_57.txt','2022_10_1_12_52.txt','2022_10_1_13_37.txt','2022_10_1_14_2.txt','2022_10_1_14_30.txt','2022_10_1_14_48.txt','2022_10_1_14_59.txt','2022_10_1_15_30.txt','2022_10_1_15_52.txt','2022_10_1_16_18.txt']

totals = {}
totals_n = {}
for file in files:
    # convert file name to timestamp here if I want
    with open('outage_data/'+file,'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            i = 0
            while row[0][i] != ':':
                i += 1
            zipcode = int(row[0][i+2:-1])
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
            totals[zipcode] += n
            totals_n[zipcode] += n/n_t

with open('totals/sum.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Zipcode','Customer-5mins','Av time per customer (5mins)'])
    for z in totals:
        writer.writerow([z,totals[z],totals_n[z]])
            