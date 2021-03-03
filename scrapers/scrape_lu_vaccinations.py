#!/usr/bin/env python3

import re
import arrow
from bs4 import BeautifulSoup
import xlrd
import scrape_common as sc


def parse_lu_date(date_str):
    return arrow.get(date_str, 'DD.MM.YYYY', locale='de').datetime.date()


base_url = 'https://www.lustat.ch'
url = f'{base_url}/daten?id=28177'
d = sc.download(url)
soup = BeautifulSoup(d, 'html.parser')

link = soup.find('a', href=re.compile(r'.xlsx$'))
xls_url = link.get('href')
if not xls_url.startswith('http'):
    xls_url = f'{base_url}{xls_url}'
xls_data = sc.download_data(xls_url)

book = xlrd.open_workbook(file_contents=xls_data)
sheet = book.sheet_by_index(0)

title_row = 5
date_column = 0
first_dose_column = 11
second_dose_column = 13

first_doses = 0
second_doses = 0
for row in range(title_row + 1, sheet.nrows):
    value = sheet.cell_value(row, first_dose_column)
    if value == '...' or value == '-':
        continue

    vd = sc.VaccinationData(canton='LU', url=url)

    try:
        date = sheet.cell_value(row, date_column)
        vd.date = parse_lu_date(date)
    except:
        break

    value = sheet.cell_value(row, first_dose_column)
    if value != '-':
        first_doses += int(sheet.cell_value(row, first_dose_column))
    vd.first_doses = first_doses
    value = sheet.cell_value(row, second_dose_column)
    if value != '-':
        second_doses += int(sheet.cell_value(row, second_dose_column))
    vd.second_doses = second_doses
    vd.total_vaccinations = vd.first_doses + vd.second_doses

    assert vd
    print(vd)
