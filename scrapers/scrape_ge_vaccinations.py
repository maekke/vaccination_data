#!/usr/bin/env python3

import re
from bs4 import BeautifulSoup
import scrape_common as sc


def parse_table(table):
    trs = table.find_all('tr')
    total_vaccinations = 0
    result = {}
    for tr in trs[1:]:
        tds = tr.find_all('td')
        assert len(tds) == 2, f'Expected 2 columns, but got: {tds}'
        res = re.search(r'\s?(\d+)\s?', tds[1].text)
        assert res
        weekly_vaccinations = int(res[1])

        res = re.search(r'(Cumul des) .* doses', tds[0].text)
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

        if not year:
            year = 2021

        total_vaccinations = weekly_vaccinations + total_vaccinations
        result[f'{year}-{week}'] = (year, week, total_vaccinations)
    return result


url = 'https://www.ge.ch/se-faire-vacciner-contre-covid-19/vaccination-chiffres'
d = sc.download(url)
d = re.sub(r'(\d+)\'(\d+)', r'\1\2', d)
soup = BeautifulSoup(d, 'html.parser')

table = soup.find('h5', string=re.compile('1.re dose')).find_next('table').find_next('table')
first_doses = parse_table(table)

table = soup.find('h5', string=re.compile('2nde dose')).find_next('table').find_next('table')
second_doses = parse_table(table)

vds = {}
for key, values in first_doses.items():
    vd = sc.VaccinationData(canton='GE', url=url)
    vd.year = values[0]
    vd.week = values[1]
    vd.first_doses = values[2]
    vd.total_vaccinations = int(vd.first_doses)
    vds[key] = vd

for key, values in second_doses.items():
    vd = vds[key]
    vd.second_doses = values[2]
    vd.total_vaccinations = int(vd.first_doses) + int(vd.second_doses)

for key, values in vds.items():
    print(values)
