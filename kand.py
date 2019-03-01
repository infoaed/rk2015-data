#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import random
import requests
import bs4
import string
import csv
import time
import re

min = 101
max = 101+1099
amount = 1099

random.seed(123)

#data = random.sample(range(min, max), amount)
data = range(min, max)

j=0

def validate_mobile(value):
    if value.startswith("Tel "):
        rule = re.compile(r'^[0-9 +-,]+$')
        return rule.search(value[4:]) is not None
    else:
        return False

def validate_email(value):
    if value.startswith("E-post "):
        rule = re.compile(r'^.+@.+$')
        return rule.search(value[7:]) is not None
    else:
        return False

with open('urlid.txt', 'r') as knd_file:
    knd_list = knd_file.readlines()
knd_file.close()

for url in knd_list:
    j+=1
    #if j>10: break
    #print(url)
    succ = 1
    while succ > 0:
        try:
            page = requests.get(url)
            succ = 0
        except requests.exceptions.RequestException as e:
            print(e)
            succ += 1
            time.sleep(succ)
    soup = bs4.BeautifulSoup(page.content, 'lxml')
    dist = soup.find_all("article", {"class", "station-info"})
    #dist = soup.find_all("span", {"class", "breadcrumb-item active"})
    #print(dist)
    candnr = dist[0].text.split("Kandidaat nr ")[-1].split(" ")[0]
    candname = dist[0].find_all("span", {"class", "uppercase"})
    ringkond = url.split("kandidaadid/")[1].split("/")[0]
    nimi = candname[0].text.title()
    
    #print(nimi, candnr, ringkond)
    

    table = soup.find(name='dl')
    if table is None:
        print("%d: " % i)
        continue;
    rows = table.find_all('dt')
    cols = table.find_all('dd')
    
    res = [candnr, ringkond, nimi]

    for row, col in zip(rows, cols):
        rt= row.text.strip()
        ct = col.text.strip()
        
        if rt=='Nimekiri või üksikkandidaat:':
            nimek = ct
        elif rt=='Sünniaeg:':
            synd = ct
        elif rt=='Erakondlik kuuluvus:':
            erak = ct
        elif rt=='Kontaktandmed:':
            kontakt = ct
        elif rt=='Haridus:':
            harid = ct
        elif rt=='Töökoht ja amet:':
            amet = ct

    res = [candnr, ringkond, nimi, nimek, synd, erak, harid, amet ]

    #print(rows, cols)

    #print(res)

    mob = ""
    email = ""
    addr = ""
    k=kontakt
    if validate_mobile(k):
        mob = k[4:].strip() # "Tel: "
    elif validate_email(k):
        email = k[7:].strip() # "E-post: "
    else:
        addr = k[8:].strip() # "Aadress: "


#        for col in cols:
#            k+=1
#            raw=col.text
#            if len(raw)==0 or raw in ["Andmed"]:
#                break;
#            print(raw)
#            if k==2: break
    
    #print(nimi)
    #print (nimi, len(k), k)


#    for k in kont:
#        if validate_mobile(k):
#            print(" > " + k)
#        elif validate_email(k):
#            print(" = " + k)
#        else:
#            print(" & " + k.strip())

    res.append(mob)
    res.append(email)
    res.append(addr)
    print(j)
    with open('rk2015-kandidaadid.csv', 'a') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(res)
    csv_file.close()

