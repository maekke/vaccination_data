#!/usr/bin/env python3

import re
import arrow
from bs4 import BeautifulSoup
import scrape_common as sc


def parse_ti_date(date_str):
    return arrow.get(date_str, 'DD.MM.YYYY', locale='de').datetime.date()


url = 'https://www4.ti.ch/dss/dsp/covid19/home/'
d = sc.download(url)
d = re.sub(r'(\d+)\'(\d+)', r'\1\2', d)
d = re.sub(r'(\d+)&#039;(\d+)', r'\1\2', d)
soup = BeautifulSoup(d, 'html.parser')

vd = sc.VaccinationData(canton='TI', url=url)

element = soup.find('h2', string=re.compile('Vaccinazione')).find_next('div')
res = re.search(r'Stato: (\d+.\d+.\d{4})', element.text)
assert res
vd.date = parse_ti_date(res[1])

element = soup.find('div', string='Totale numero dosi somministrate')
element = element.find_previous('div')
vd.total_vaccinations = int(element.text.strip())

element = soup.find('div', string=re.compile(r'Numero persone con vaccinazione\s+completa\s+\(2 dosi\)'))
element = element.find_previous('div')
vd.second_doses = int(element.text.strip())

vd.first_doses = vd.total_vaccinations - vd.second_doses

assert vd
print(vd)
