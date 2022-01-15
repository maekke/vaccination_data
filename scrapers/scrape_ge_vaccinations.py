#!/usr/bin/env python3

import datetime
import re
import arrow
from bs4 import BeautifulSoup
import scrape_common as sc


def parse_ge_date(date_str):
    date = arrow.get(date_str, 'D MMMM YYYY', locale='fr')
    return datetime.date(year=date.year, month=date.month, day=date.day).isoformat()


url = 'https://www.ge.ch/teaser/covid-19-vaccin'
d = sc.download(url)
d = re.sub(r'(\d+)\'(\d+)', r'\1\2', d)
d = re.sub(r'(\d+)’(\d+)', r'\1\2', d)
d = d.replace(u'\xa0', u' ')
d = d.replace(u'<br />', u' ')
soup = BeautifulSoup(d, 'html.parser')

vd = sc.VaccinationData(canton='GE', url=url)

date_re = 'Chiffres au (\d+\s+.*\d{4})'
elem = soup.find('em', text=re.compile(date_re))
assert elem
res = re.search(date_re, elem.string)
assert res
vd.date = parse_ge_date(res[1])

elem = soup.find_all('div', text=re.compile('^\s+\d+\s+'))
assert len(elem) == 5

vd.first_doses = int(elem[0].text.strip())
vd.second_doses = int(elem[1].text.strip())
vd.total_vaccinations = int(elem[4].text.strip())

assert vd
print(vd)
