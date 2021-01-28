#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from bs4 import BeautifulSoup
import scrape_common as sc

base_url = 'https://www.jura.ch'
url = f'{base_url}/fr/Autorites/Coronavirus/Chiffres-H-JU/Evolution-des-cas-COVID-19-dans-le-Jura.html'
d = sc.download(url)
d = d.replace('&nbsp;', ' ')
soup = BeautifulSoup(d, 'html.parser')

pdf_url = soup.find('a', title=re.compile(r'.*PDF.*')).get('href')
if not pdf_url.startswith('http'):
    pdf_url = f'{base_url}{pdf_url}'
pdf_url = pdf_url.replace('?download=1', '')

pdf = sc.download_data(pdf_url)
pages = sc.pdfinfo(pdf)

vd = sc.VaccinationData(canton='JU', url=pdf_url)

content = sc.pdf_to_text(pdf, page=1)
res = re.search(r'Situation semaine .pid.miologique (\d+)', content)
assert res
vd.week = res[1]

res = re.search(r'Du \d+.* (\d{4})', content)
assert res
vd.year = res[1]

content = sc.pdf_to_text(pdf, page=pages, layout=True)

# get last total (total of all vaccinations)
pos = content.rfind('Total')
assert pos > 0
content = content[pos:]

res = re.search(r'Total\s+\d+\s+\d+\s+\d+\s+(\d+)', content)
assert res
vd.total_vaccinations = res[1]

print(vd)
