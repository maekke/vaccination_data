#!/usr/bin/env python3

import arrow
import re
from bs4 import BeautifulSoup
import scrape_common as sc


def parse_so_date(date_str):
    return arrow.get(date_str, 'DD.M.YYYY', locale='de').datetime.date()


url = 'https://corona.so.ch/bevoelkerung/daten/impfstatistik/'
d = sc.download(url)
soup = BeautifulSoup(d, 'html.parser')

title = soup.find('h3', string=re.compile(r'^Stand \d+\.')).text
res = re.search(r'Stand (\d+\.\d+\.20\d{2}),', title)
assert res
date = res[1]
date = parse_so_date(date)

element = soup.find('td', string=re.compile('Anzahl Impfungen \(kumuliert\)'))
element = element.find_next('td')

vd = sc.VaccinationData(canton='SO', url=url)
vd.date = date.isoformat()
vd.total_vaccinations = element.text.replace("'", "")
assert vd
print(vd)
