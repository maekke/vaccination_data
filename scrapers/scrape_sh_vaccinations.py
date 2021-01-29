#!/usr/bin/env python3

import datetime
import json
import arrow
import xlrd
from bs4 import BeautifulSoup
import scrape_common as sc


def parse_be_date(date_str):
    return arrow.get(date_str, 'DD.MM.YY', locale='de').datetime.date()


base_url = 'https://sh.ch'
main_url = f'{base_url}/CMS/Webseite/Kanton-Schaffhausen/Beh-rde/Verwaltung/Departement-des-Innern/Gesundheitsamt-3209198-DE.html'
url = f'{base_url}/CMS/content.jsp?contentid=3666465&language=DE&_=1611921384916'
d = sc.download_json(url)
d = json.loads(d['data_filemeta'])
url = f"{base_url}{d['url']}"

xls_data = sc.download_data(url)
book = xlrd.open_workbook(file_contents=xls_data)
sheet = book.sheet_by_name('Tabelle1')

start_row = 1
date_column = 0
first_dose_column = 11
second_dose_column = 12

for row in range(start_row, sheet.nrows):
    value = sheet.cell_value(row, first_dose_column)
    if value is None or value == '':
        continue

    vd = sc.VaccinationData(canton='SH', url=main_url)

    date = sheet.cell_value(row, date_column)
    date = datetime.datetime(*xlrd.xldate_as_tuple(date, book.datemode))
    vd.date = date.date().isoformat()

    vd.first_doses = int(sheet.cell_value(row, first_dose_column))
    vd.second_doses = int(sheet.cell_value(row, second_dose_column))
    vd.total_vaccinations = vd.first_doses + vd.second_doses

    assert vd
    print(vd)
