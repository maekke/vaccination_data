#!/usr/bin/env python3

import datetime
import re
import arrow
from bs4 import BeautifulSoup
import scrape_common as sc


def parse_ge_date(date_str):
    date = arrow.get(date_str, 'D MMMM YYYY', locale='fr')
    return datetime.date(year=2021, month=date.month, day=date.day).isoformat()


url = 'https://www.ge.ch/se-faire-vacciner-contre-covid-19/vaccination-chiffres'
d = sc.download(url)
d = re.sub(r'(\d+)\'(\d+)', r'\1\2', d)
d = d.replace(u'\xa0', u' ')
soup = BeautifulSoup(d, 'html.parser')

vd = sc.VaccinationData(canton='GE', url=url)

tot_vacc_re = r'(\d+) doses ont .* au (\d+\s+\w+\s+\d{4})'
element = soup.find('p', text=re.compile(tot_vacc_re))
assert element
res = re.search(tot_vacc_re, element.text)
assert res
vd.date = parse_ge_date(res[2])
vd.total_vaccinations = int(res[1])

res = re.search(r'.*\s+(\d+)\s+personnes\s+ont\s+re.u\s+la\s+1.*', d)
assert res
vd.first_doses = int(res[1])

res = re.search(r'.*\s+(\d+)\s+personnes\s+ont\s+re.u\s+leur\s+2.*', d)
assert res
vd.second_doses = int(res[1])

assert vd
print(vd)
