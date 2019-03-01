#!/bin/bash
for i in {0..12}
do
   wget "http://info.rk2015.vvk.ee/kandidaadid/$i/" -O ->> index.html
done
grep "href=\"/kandidaadid/" index.html | grep strong | sed -E 's/(.*)(<a href=\")([^\"]*)(.*)/http:\/\/info.rk2015.vvk.ee\3/' | sort -u > urlid.txt
