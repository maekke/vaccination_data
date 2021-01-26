#!/usr/bin/env python3

import re
from bs4 import BeautifulSoup
import scrape_common as sc

url = 'https://www.ge.ch/se-faire-vacciner-contre-covid-19/vaccination-chiffres'
d = sc.download(url)
d = re.sub(r'(\d+)\'(\d+)', r'\1\2', d)
soup = BeautifulSoup(d, 'html.parser')

table = soup.find('strong', string=re.compile('VACCINATIONS CONTRE LA COVID-19 PAR SEMAINE')).find_next('table')
trs = table.find_all('tr')
total_vaccinations = 0
for tr in trs[1:]:
    tds = tr.find_all('td')
    assert len(tds) == 2, f'Expected 2 columns, but got: {tds}'
    res = re.search(r'\s?(\d+)\s?', tds[1].text)
    assert res
    weekly_vaccinations = int(res[1])

    res = re.search(r'(Cumul des vaccinations)', tds[0].text)
    if res:
        assert weekly_vaccinations == total_vaccinations, f'expected {weekly_vaccinations}, but got {total_vaccinations}'
        continue

    week = None
    res = re.search(r'Semaine (\d+)', tds[0].text)
    if res:
        week = res[1]

    year = None
    res = re.search(r'\s\d+\.\d+\.(\d{4})', tds[0].text)
    if res:
        year = res[1]

    if not week and re.search(r'(D.cembre 2020)', tds[0].text):
        # let's use the last week of the year
        week = 53
        year = 2020

    vd = sc.VaccinationData(canton='GE', url=url)
    vd.week = week
    vd.year = year
    vd.total_vaccinations = weekly_vaccinations + total_vaccinations
    total_vaccinations = vd.total_vaccinations
    print(vd)
