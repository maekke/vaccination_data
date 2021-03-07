#!/usr/bin/env python3

import re
import arrow
from bs4 import BeautifulSoup
import scrape_common as sc


def parse_ow_date(date_str):
    return arrow.get(date_str, 'DD.MM.YYYY', locale='de').datetime.date()


url = 'https://www.ow.ch/de/verwaltung/dienstleistungen/?dienst_id=5962'
d = sc.download(url)
d = re.sub(r'(\d+)\'(\d+)', r'\1\2', d)
d = re.sub(r'(\d+) (\d+)', r'\1\2', d)
d = re.sub(r'&nbsp;', r' ', d)
soup = BeautifulSoup(d, 'html.parser')

vd = sc.VaccinationData(canton='OW', url=url)

res = re.search(r'Impfung \(Stand (\d+\.\d+\.\d{4})\)', d)
assert res
vd.date = parse_ow_date(res[1])

element = soup.find('p', string=re.compile('Bislang haben'))
res = re.search(r'Bislang haben rund (\d+)', element.text)
assert res
vd.first_doses = int(res[1])
vd.second_doses = int(res[1])
vd.total_vaccinations = vd.first_doses + vd.second_doses

print(vd)
