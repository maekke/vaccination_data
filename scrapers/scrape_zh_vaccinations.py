#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import arrow
from bs4 import BeautifulSoup
import scrape_common as sc


def parse_zh_date(date_str):
    return arrow.get(date_str, 'D. MMMM YYYY', locale='de').datetime.date().isoformat()


base_url = 'https://www.zh.ch'
url = f'{base_url}/de/gesundheit/coronavirus.html'
content = sc.download(url)
content = re.sub(r'(\d+)\'(\d+)', r'\1\2', content)
soup = BeautifulSoup(content, 'html.parser')

vd = sc.VaccinationData(canton='ZH', url=url)

date_re = r'Diese Zahlen wurden am (\d+\.\s+\w+\s+\d{4})'
element = soup.find('span', string=re.compile(date_re))
res = re.search(date_re, element.text)
assert res
vd.date = parse_zh_date(res[0])

element = soup.find('th', string=re.compile(r'Total verabreichte Impfdosen'))
element = element.find_next('td')
vd.total_vaccinations = int(element.text)

element = soup.find('th', string=re.compile(r'1. Impfdosis'))
element = element.find_next('td')
vd.first_doses = int(element.text)

element = soup.find('th', string=re.compile(r'2. Impfdosis'))
element = element.find_next('td')
vd.second_doses = int(element.text)

assert vd
print(vd)
