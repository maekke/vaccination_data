#!/usr/bin/env python3

import re
import arrow
from bs4 import BeautifulSoup
import scrape_common as sc


def parse_ow_date(date_str):
    return arrow.get(date_str, 'D. MMMM YYYY', locale='de').datetime.date()


def get_column(tr):
    tds = tr.find_all('td')
    assert len(tds) == 2, f'expected two td items: {tds}'
    return int(tds[1].text)


url = 'https://www.ow.ch/de/verwaltung/dienstleistungen/?dienst_id=5962'
d = sc.download(url, encoding='windows-1252')
d = re.sub(r'(\d+)\'(\d+)', r'\1\2', d)
d = re.sub(r'(\d+) (\d+)', r'\1\2', d)
d = re.sub(r'&nbsp;', r' ', d)
soup = BeautifulSoup(d, 'html.parser')

vd = sc.VaccinationData(canton='OW', url=url)

date_regex = r'Die Impfstatistik des Kantons Obwalden \(zuletzt aktualisiert: (\d+\.\s+\w+\s+\d{4})\)'
element = soup.find('em', string=re.compile(date_regex))
assert element
res = re.search(date_regex, element.text)
assert res
vd.date = parse_ow_date(res[1])

element = element.find_next('table')

trs = element.find_all('tr')
assert len(trs) == 4, f'unexpected number of rows: {trs}'

vd.doses_delivered = get_column(trs[0])
vd.first_doses = get_column(trs[1])
vd.second_doses = get_column(trs[2])
vd.total_vaccinations = get_column(trs[3])

assert vd
print(vd)
