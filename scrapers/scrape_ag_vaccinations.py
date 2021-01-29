#!/usr/bin/env python3

import datetime
import re
from bs4 import BeautifulSoup
import xlrd
import scrape_common as sc


base_url = 'https://www.ag.ch'
url = f'{base_url}/de/themen_1/coronavirus_2/lagebulletins/lagebulletins_1.jsp'
d = sc.download(url)
soup = BeautifulSoup(d, 'html.parser')

link = soup.find('a', href=re.compile(r'.xlsx$'))
xls_url = link.get('href')
if not xls_url.startswith('http'):
    xls_url = f'{base_url}{xls_url}'
xls_data = sc.download_data(xls_url)

book = xlrd.open_workbook(file_contents=xls_data)
sheet = book.sheet_by_name('6. Impfkampagne')

title_row = 2
date_column = 0

first_dose_column = None
second_dose_column = None
total_vaccinations_column = None
doses_delivered_column = None
for column in range(title_row, sheet.ncols):
    value = sheet.cell_value(2, column)
    if value == 'Total Erstimpfungen (kumuliert)':
        first_dose_column = column
    if value == 'Total Zweitimpfungen (kumuliert)':
        second_dose_column = column
    if value == 'Total Impfungen (kumuliert)':
        total_vaccinations_column = column
    if value == 'Anzahl gelieferte Impfdosen (kumuliert) (TOTAL)':
        doses_delivered_column = column

assert first_dose_column
assert second_dose_column
assert total_vaccinations_column
assert doses_delivered_column

for row in range(title_row + 1, sheet.nrows):
    value = sheet.cell_value(row, first_dose_column)
    if value is None or value == '':
        continue

    vd = sc.VaccinationData(canton='AG', url=url)

    date = sheet.cell_value(row, date_column)
    cell_type = sheet.cell_type(row, date_column)
    if cell_type == 1:
        vd.week = int(re.search(r'KW(\d+)', date)[1])
        vd.year = 2021
        if vd.week == 53:
            vd.year = 2020
    else:
        date = datetime.datetime(*xlrd.xldate_as_tuple(date, book.datemode))
        vd.date = date.date().isoformat()

    vd.total_vaccinations = int(sheet.cell_value(row, total_vaccinations_column))
    vd.first_doses = int(sheet.cell_value(row, first_dose_column))
    vd.second_doses = int(sheet.cell_value(row, second_dose_column))
    vd.doses_delivered = int(sheet.cell_value(row, doses_delivered_column))

    assert vd
    print(vd)
