#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import arrow
from bs4 import BeautifulSoup
import scrape_common as sc


def parse_vs_date(date_str):
    return arrow.get(date_str, 'DD/MM/YYYY', locale='de').datetime.date()


base_url = 'https://www.vs.ch'
url = f'{base_url}/web/coronavirus/statistiques'
content = sc.download(url)
soup = BeautifulSoup(content, 'html.parser')

pdf_urls = []
links = soup.find_all('a', href=re.compile(r'2021 .* Sit Epid'))
for link in links:
    url = link.get('href')
    if not url.startswith('http'):
        url = f'{base_url}{url}'
    pdf_urls.append(url)

for pdf_url in pdf_urls:
    pdf = sc.download_data(pdf_url)
    content = sc.pdf_to_text(pdf, layout=True, page=1)

    res = re.search(r'(\d{2}/\d{2}/20\d{2})', content)
    assert res
    date = res[1]
    date = parse_vs_date(date)
    if date.year == 2020:
        # no data available in 2020
        break

    vd = sc.VaccinationData(canton='VS', url=pdf_url)
    vd.date = date.isoformat()
    res = re.search(r'.*Anzahl\s+der\s+\w+\s+Impfdosen.*\s+(\d+.\d+)\s+', content)
    if not res:
        # no data available in oder PDFs
        # (latest are processed first)
        break
    vd.total_vaccinations = re.sub(r'[^0-9]', '', res[1])
    if vd:
        print(vd)
