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
    
for i in range(1, 13):
    j+=1
    #if j>10: break
    url=("http://rk2015.vvk.ee/detailed-%d.html") % i
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
    dist = soup.find_all("table", {"class", "mandates detailed-party"})
    #print(dist)
#    ringkond = dist[0].text.split(" ")[-1]
#    candname = soup.find_all("span", {"class", "uppercase"})
#    nimi = candname[0].text.title()

    heads = []

    table = dist[0].find('tr', {'class', "header-blue"})
    #print(table)
    hhh = table.find_all("th")
    for h in hhh:
        heads.append(h.text)

    print(heads)

    #exit(1)
    for di in dist:
        table = di.find(name='tbody')
        rrr = table.find_all("tr")
        for r in rrr:
            if r.text.find("Nimekiri kokku") < 0:
                #print(r)
                td = 0
                res = []
                ddd = r.find_all("td")
                for d in ddd:
                    if heads[td]=="Jrk nr":
                        print(heads[td], d.text)
                    elif heads[td]=="Reg nr":
                        print(heads[td], d.text)
                        res.append(d.text)
                    elif heads[td]=="Kandidaat":
                        print(heads[td], d.text.title())
                        res.append(d.text.title())
                    elif heads[td]=="Kokku":
                        print(heads[td], d.text.strip())
                        res.append(d.text.strip())
                    elif heads[td]=="Hääled välisriigist":
                        print(heads[td], d.text)
                        res.append(d.text.strip())
                    elif heads[td]=="E-hääled*":
                        print(heads[td], d.text)
                        res.append(d.text.strip())
                    else:
                        print(heads[td], d.text)
                    td += 1

                with open('rk2015-tulemused.csv', 'a') as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(res)
                csv_file.close()


