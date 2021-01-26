#!/usr/bin/env python3

import re
import arrow
from bs4 import BeautifulSoup
import scrape_common as sc


def parse_be_date(date_str):
    return arrow.get(date_str, 'DD.MM.YY', locale='de').datetime.date()


url = 'https://www.besondere-lage.sites.be.ch/de/start/impfen.html'
d = sc.download(url)
d = re.sub(r'(\d+)\'(\d+)', r'\1\2', d)
soup = BeautifulSoup(d, 'html.parser')

table = soup.find('p', string=re.compile('Durchgef.hrte Impfungen im Kanton Bern')).find_next('table')
tbody = table.find_all('tbody')[0]
trs = tbody.find_all('tr')

for tr in trs[1:]:
    tds = tr.find_all('td')
    assert len(tds) == 3, f'expected 3 rows, but got {len(tds)} ({tds})'

    vd = sc.VaccinationData(canton='BE', url=url)

    res = re.search(r'(\d+\.\d+\.\d+)', tds[0].text)
    assert res
    date = parse_be_date(res[1])
    vd.date = date.isoformat()

    res = re.search(r'(\d+)\s?', tds[1].text)
    assert res
    vd.total_vaccinations = res[1]

    res = re.search(r'(\d+)\s?', tds[2].text)
    assert(res)
    vd.second_doses = res[1]
    if vd:
        print(vd)
