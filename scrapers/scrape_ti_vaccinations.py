#!/usr/bin/env python3

import re
import arrow
from bs4 import BeautifulSoup
import scrape_common as sc


def parse_ti_date(date_str):
    return arrow.get(date_str, 'DD.MM.YYYY', locale='de').datetime.date()


url = 'https://www4.ti.ch/dss/dsp/covid19/home/'
d = sc.download(url)
soup = BeautifulSoup(d, 'html.parser')

vd = sc.VaccinationData(canton='TI', url=url)

date_regex = r'Aggiornamento dati (\d+.\d+.\d{4})'
element = soup.find('div', string=re.compile(date_regex))
date = element.text
res = re.search(date_regex, date)
assert res
vd.date = parse_ti_date(res[1])

element = soup.find('div', string=re.compile(r'Persone con vaccinazione parziale'))
element = element.find_previous('div')
vd.first_doses = int(element.text)

element = soup.find('div', string=re.compile(r'Persone con vaccinazione completa'))
element = element.find_previous('div')
vd.second_doses = int(element.text) * 2

element = soup.find('div', string=re.compile(r'Totale numero dosi somministrate'))
element = element.find_previous('div')
vd.total_vaccinations = int(element.text)

assert vd
print(vd)
