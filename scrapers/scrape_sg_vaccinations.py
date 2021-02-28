#!/usr/bin/env python3

import re
import arrow
from bs4 import BeautifulSoup
import scrape_common as sc


def parse_sg_date(date_str):
    return arrow.get(date_str, 'DD. MMMM YYYY', locale='de').datetime.date()


url = 'https://www.sg.ch/tools/informationen-coronavirus/impfung-gegen-covid-19-im-kanton-st-gallen.html'
d = sc.download(url)
d = re.sub(r'(\d+)\'(\d+)', r'\1\2', d)
soup = BeautifulSoup(d, 'html.parser')

vd = sc.VaccinationData(canton='SG', url=url)

element = soup.find('h3', string=re.compile(r'\*\*\*\s+News'))
element = element.find_next('p')
res = re.search(r'\d+\.\s+\w+\s+(\d{4})', element.text)
assert res
year = res[1]

res = re.search(r'Bis\s+zum\s+(\d+\.\s+)\w+', element.text)
assert res
date = res[0]
vd.date = parse_sg_date(f'{date} {year}')

vaccinations = re.findall(r'(\d+) Impfungen', element.text)
vd.total_vaccinations = 0
for vaccination in vaccinations:
    vd.total_vaccinations += int(vaccination)

assert vd
print(vd)
