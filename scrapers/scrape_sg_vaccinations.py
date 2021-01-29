#!/usr/bin/env python3

import re
from bs4 import BeautifulSoup
import scrape_common as sc


url = 'https://www.sg.ch/tools/informationen-coronavirus/impfung-gegen-covid-19-im-kanton-st-gallen.html'
d = sc.download(url)
d = re.sub(r'(\d+)\'(\d+)', r'\1\2', d)
soup = BeautifulSoup(d, 'html.parser')

vd = sc.VaccinationData(canton='SG', url=url)

element = soup.find('h3', string=re.compile('Impf-Fortschritt')).find_next('h4')

# on 2021-01-29 there is also a news item with the same value
# maybe worth checking to use the dates at some point
res = re.search(r'Stand KW (\d+):', element.text)
assert res
vd.week = res[1]
vd.year = 2021

element = element.find_next('p')
res = re.findall(r'\w+: (\d+)\s?', element.text)
assert len(res) > 0
vd.total_vaccinations = 0
for value in res:
    vd.total_vaccinations += int(value)

assert vd
print(vd)
