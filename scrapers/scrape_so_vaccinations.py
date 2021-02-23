#!/usr/bin/env python3

import re
import arrow
from bs4 import BeautifulSoup
import scrape_common as sc


def parse_so_date(date_str):
    return arrow.get(date_str, 'DD.MM.YYYY', locale='de').datetime.date()


url = 'https://corona.so.ch/index.php?id=27979'
d = sc.download(url)
soup = BeautifulSoup(d, 'html.parser')

table = soup.find('h2', string=re.compile(r'Situation Kanton Solothurn')).find_next('table')

headers = table.find_all('th')
vaccination_index = None
for i in range(0, len(headers)):
    if headers[i].text == 'Anzahl Impfungen (Erstimpfung)':
        vaccination_index = i

assert vaccination_index, f'Failed to find vaccinations in {headers}'

rows = table.find('tbody').find_all('tr')
for row in rows:
    tds = row.find_all('td')
    value = tds[vaccination_index].text
    res = re.search(r'(\d+)', value)
    if res:
        vd = sc.VaccinationData(canton='SO', url=url)
        vd.first_doses = res[1]
        vd.total_vaccinations = res[1]

        date = parse_so_date(tds[0].text)
        vd.date = date.isoformat()
        print(vd)
