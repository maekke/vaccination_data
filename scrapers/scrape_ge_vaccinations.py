#!/usr/bin/env python3

import datetime
import re
import arrow
from bs4 import BeautifulSoup
import scrape_common as sc


def parse_ge_date(date_str):
    date = arrow.get(date_str, 'D MMMM YYYY', locale='fr')
    return datetime.date(year=date.year, month=date.month, day=date.day).isoformat()


url = 'https://www.ge.ch/document/covid-19-chiffres-campagne-vaccination-geneve'
d = sc.download(url)
d = re.sub(r'(\d+)\'(\d+)', r'\1\2', d)
d = re.sub(r'(\d+)’(\d+)', r'\1\2', d)
d = re.sub(r'(\d+)\'(\d+)', r'\1\2', d)
soup = BeautifulSoup(d, 'html.parser')

vd = sc.VaccinationData(canton='GE', url=url)

date_re = 'au (\d+\s+.*\d{4})'
elem = soup.find('h4', string=re.compile('^Chiffres .*'))
assert elem
elem = elem.find_next('p')
assert elem
res = re.search(date_re, elem.text)
assert res
vd.date = parse_ge_date(res[1])

res = re.search('de\s+(\d+)\s+au', elem.text)
assert res
vd.total_vaccinations = int(res[1])

doses_regex = '(\d+)\s+personnes'

elem = soup.find('li', string=re.compile('^(\d+)\s+.*premi.re\s+dose'))
assert elem
res = re.search(doses_regex, elem.text)
assert res
vd.first_doses = int(res[1])

elem = soup.find('li', string=re.compile('^(\d+)\s+.*deuxi.me\s+dose'))
assert elem
res = re.search(doses_regex, elem.text)
assert res
vd.second_doses = int(res[1])

assert vd
print(vd)
