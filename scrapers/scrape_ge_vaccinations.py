#!/usr/bin/env python3

import datetime
import re
import arrow
from bs4 import BeautifulSoup
import scrape_common as sc


def parse_ge_date(date_str):
    date = arrow.get(date_str, 'DD.MM', locale='de')
    return datetime.date(year=2021, month=date.month, day=date.day).isoformat()


def extract_values(element):
    res = re.search(r'(\d+)\s?', element.text)
    assert res
    doses = int(res[1])

    res = re.search(r'chiffres au (\d+\.\d+)', element.text)
    assert res
    date = parse_ge_date(res[1])

    return (date, doses)


url = 'https://www.ge.ch/se-faire-vacciner-contre-covid-19/vaccination-chiffres'
d = sc.download(url)
d = re.sub(r'(\d+)\'(\d+)', r'\1\2', d)
soup = BeautifulSoup(d, 'html.parser')

vds = {}

element = soup.find(text=re.compile(r'Cumul des 1')).find_next('td')

vd = sc.VaccinationData(canton='GE', url=url)
date, doses = extract_values(element)
vd.date = date
vd.first_doses = doses

element = soup.find('strong', text=re.compile(r'^\d+$'))
assert element
vd.total_vaccinations = int(element.text)
vds[vd.date] = vd

element = soup.find(text=re.compile(r'Cumul des 2')).find_next('td')
date, doses = extract_values(element)
if date == vd.date:
    vd.second_doses = doses
    assert vd.first_doses + vd.second_doses == vd.total_vaccinations

for key, values in vds.items():
    print(values)
