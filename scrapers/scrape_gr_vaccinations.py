#!/usr/bin/env python3

import re
import arrow
from bs4 import BeautifulSoup
import scrape_common as sc


def parse_gr_date(date_str):
    return arrow.get(date_str, 'DD.MM.YYYY', locale='de').datetime.date()


url = 'https://www.gr.ch/DE/institutionen/verwaltung/djsg/ga/coronavirus/info/impfen/Seiten/impfen.aspx'
d = sc.download(url)
d = re.sub(r'(\d+)\s(\d+)', r'\1\2', d)
d = re.sub(r'(\d+)&#39;(\d+)', r'\1\2', d)
soup = BeautifulSoup(d, 'html.parser')

table = soup.find('h2', string=re.compile('Impfungen Kanton Graub.nden')).find_next('table')
tbody = table.find_all('tbody')[0]
trs = tbody.find_all('tr')

for tr in trs:
    tds = tr.find_all('td')
    assert len(tds) == 4, f'expected 4 rows, but got {len(tds)} ({tds})'

    vd = sc.VaccinationData(canton='GR', url=url)

    res = re.search(r'(\d+\.\d+\.\d+)', tds[0].text)
    assert res
    date = parse_gr_date(res[1])
    vd.date = date.isoformat()

    res = re.search(r'(\d+)\s?', tds[1].text)
    assert res
    vd.first_doses = int(res[1])

    res = re.search(r'(\d+)\s?', tds[2].text)
    assert(res)
    vd.second_doses = int(res[1])
    vd.total_vaccinations = vd.first_doses + vd.second_doses
    print(vd)
