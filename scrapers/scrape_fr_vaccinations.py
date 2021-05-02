#!/usr/bin/env python3

import re
import arrow
from bs4 import BeautifulSoup
import scrape_common as sc


def parse_fr_date(date_str):
    return arrow.get(date_str, 'DD.MM.YYYY', locale='de').datetime.date()


url = 'https://www.fr.ch/de/gesundheit/covid-19/coronavirus-statistik-ueber-die-entwicklung-im-kanton'
d = sc.download(url)
d = re.sub(r'(\d+)\'(\d+)', r'\1\2', d)
d = re.sub(r'(\d+) (\d+)', r'\1\2', d)
d = re.sub(r'&nbsp;', r' ', d)
soup = BeautifulSoup(d, 'html.parser')

vd = sc.VaccinationData(canton='FR', url=url)

element = soup.find('em', string=re.compile('aktualisiert am'))
res = re.search(r'aktualisiert am (\d+\.\d+\.\d{4})', element.text)
assert res
vd.date = parse_fr_date(res[1])

element = soup.find('strong', string=re.compile('Anzahl der erhaltenen Dosen')).find_parent('h3')
res = re.search(r'Dosen: (\d+)', element.text)
assert res
vd.doses_delivered = res[1]

element = element.find_next('p')
res = re.search(r'Davon wurden (\d+)\s+Dosen durch den Kanton verabreicht', element.text)
assert res
vd.total_vaccinations = res[1]

assert vd
print(vd)
