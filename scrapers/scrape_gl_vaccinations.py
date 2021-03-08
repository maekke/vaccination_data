#!/usr/bin/env python3

import re
import arrow
from bs4 import BeautifulSoup
import scrape_common as sc


def parse_gl_date(date_str):
    return arrow.get(date_str, 'DD.M.YYYY', locale='de').datetime.date()


url = 'https://www.gl.ch/verwaltung/finanzen-und-gesundheit/gesundheit/coronavirus.html/4817'
d = sc.download(url)
d = re.sub(r'(\d+)\'(\d+)', r'\1\2', d)
d = re.sub(r'(\d+) (\d+)', r'\1\2', d)
d = re.sub(r'&nbsp;', r' ', d)
soup = BeautifulSoup(d, 'html.parser')

vd = sc.VaccinationData(canton='GL', url=url)

element = soup.find('strong', string=re.compile('Anzahl Impfungen pro Impfstoff'))
res = re.search(r'Stand: (\d+\.\d+\.\d{4})', element.text)
assert res
vd.date = parse_gl_date(res[1])

table = element.find_next('table')
trs = table.find_all('tr')

for tr in trs:
    tds = tr.find_all('td')
    if len(tds) == 4:
        if tds[0].text == 'Total':
            vd.total_vaccinations = tds[3].text
        elif tds[0].text == '1. Impfung':
            vd.first_doses = tds[3].text
        elif tds[0].text == '2. Impfung':
            vd.second_doses = tds[3].text

assert vd
print(vd)
