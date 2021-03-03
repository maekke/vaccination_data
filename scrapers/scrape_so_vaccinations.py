#!/usr/bin/env python3

import re
import arrow
from bs4 import BeautifulSoup
import scrape_common as sc


def parse_so_date(date_str):
    return arrow.get(date_str, 'DD.MM.YYYY', locale='de').datetime.date()


url = 'https://corona.so.ch/bevoelkerung/daten/impfstatistik/'
d = sc.download(url)
d = re.sub(r'(\d+)\'(\d+)', r'\1\2', d)
soup = BeautifulSoup(d, 'html.parser')

table = soup.find('h2', string=re.compile(r'Impfstatistik')).find_next('table')

headers = table.find_all('th')
date_index = None
tot_vaccination_index = None
first_vaccination_index = None
second_vaccination_index = None
for i in range(0, len(headers)):
    if headers[i].text.find('Verimpfte Dosen total') >= 0:
        tot_vaccination_index = i
    elif headers[i].text.find('Anzahl Dosen erste Impfung') >= 0:
        first_vaccination_index = i
    elif headers[i].text.find('Anzahl Dosen zweite Impfung') >= 0:
        second_vaccination_index = i
    elif headers[i].text.find('Datum') >= 0:
        date_index = i

assert tot_vaccination_index is not None, f'Failed to find total index in {headers}'
assert first_vaccination_index is not None, f'Failed to find first index in {headers}'
assert second_vaccination_index is not None, f'Failed to find second index in {headers}'
assert date_index is not None, f'Failed to find date index in {headers}'

rows = table.find('tbody').find_all('tr')
for row in rows:
    tds = row.find_all('td')

    vd = sc.VaccinationData(canton='SO', url=url)

    date = tds[date_index].text
    res = re.search(r'(\d+\.\d+\.\d{4}),', date)
    assert res
    vd.date = parse_so_date(res[1])

    vd.first_doses = tds[first_vaccination_index].text
    vd.second_doses = tds[second_vaccination_index].text
    vd.total_vaccinations = tds[tot_vaccination_index].text

    print(vd)
