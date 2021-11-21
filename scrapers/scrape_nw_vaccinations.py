#!/usr/bin/env python3

import re
import arrow
from bs4 import BeautifulSoup
import scrape_common as sc


def parse_nw_date(date_str):
    date_str = date_str.replace(u'\xa0', u' ')
    return arrow.get(date_str, 'D. MMMM YYYY', locale='de').datetime.date()


url = 'https://www.nw.ch/gesundheitsamtdienste/6044'
d = sc.download(url)
d = re.sub(r'(\d+)\'(\d+)', r'\1\2', d)
soup = BeautifulSoup(d, 'html.parser')

vd = sc.VaccinationData(canton='NW', url=url)

elem = soup.find(string=re.compile(r'.*zuletzt aktualisiert:.*'))
res = re.search(r'(\d+\.\s+\w+ \d{4})', elem.string)
assert res
date = res[1]
date = parse_nw_date(date)
vd.date = date.isoformat()

table = elem.find_previous('table')
trs = table.find_all('tr')
third_doses = 0
for tr in trs:
    tds = tr.find_all('td')
    assert len(tds) == 2, f'expected 2 items, got: {tds}'

    if re.search('(Bisher zugeteilte Impfdosen)', tds[0].text):
        vd.doses_delivered = int(tds[1].text)

    if re.search('(\(1. Impfung)', tds[0].text):
        vd.first_doses = int(tds[1].text)

    if re.search('(\(2. Impfung)', tds[0].text):
        vd.second_doses = int(tds[1].text)

    if re.search('(Verabreichte Auffrischimpfungen)', tds[0].text):
        third_doses = int(tds[1].text)

vd.total_vaccinations = vd.first_doses + vd.second_doses + third_doses

assert vd
print(vd)
