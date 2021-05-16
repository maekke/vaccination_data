#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import arrow
from bs4 import BeautifulSoup
import scrape_common as sc


def parse_ju_date(date_str):
    return arrow.get(date_str, 'DD.MM.YYYY', locale='de').datetime.date()


base_url = 'https://www.jura.ch'
url = f'{base_url}/fr/Autorites/Coronavirus/Infos-Actualite/Statistiques-COVID/Evolution-des-cas-COVID-19-dans-le-Jura.html'
d = sc.download(url)
d = d.replace('&nbsp;', ' ')
soup = BeautifulSoup(d, 'html.parser')

pdf_url = soup.find('a', title=re.compile(r'Donn.es de vaccination')).get('href')
if not pdf_url.startswith('http'):
    pdf_url = f'{base_url}{pdf_url}'
pdf_url = pdf_url.replace('?download=1', '')

pdf = sc.download_data(pdf_url)
pages = sc.pdfinfo(pdf)

vd = sc.VaccinationData(canton='JU', url=pdf_url)

content = sc.pdf_to_text(pdf, page=1, raw=True)
content = re.sub(r'(\d+)\'(\d+)', r'\1\2', content)
res = re.search(r'\d+\.\d+\.\d{4}\s(\d+\.\d+\.\d{4})', content)
assert res
vd.date = parse_ju_date(res[1])

res = re.search(r'(\d+)\s+Injections administr.es', content)
assert res
vd.total_vaccinations = res[1]


content = sc.pdf_to_text(pdf, page=2, raw=True)
content = re.sub(r'(\d+)\'(\d+)', r'\1\2', content)

res = re.search(r'\n(\d+)\n+Nombre de 1.re injection\n', content)
assert res
vd.first_doses = res[1]

res = re.search(r'\n(\d+)\n+Nombre de 2.me injection\n', content)
assert res
vd.second_doses = res[1]

assert vd
print(vd)
