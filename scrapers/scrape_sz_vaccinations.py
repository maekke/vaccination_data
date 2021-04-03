#!/usr/bin/env python3

import datetime
import re
import arrow
from bs4 import BeautifulSoup
import xlrd
import scrape_common as sc


url = 'https://www.sz.ch/behoerden/information-medien/medienmitteilungen/coronavirus.html/72-416-412-1379-6948'
d = sc.download(url)
soup = BeautifulSoup(d, 'html.parser')

link = soup.find('a', text=re.compile(r'Kennzahlen Impfungen'))
xls_url = link.get('href')
xls_data = sc.download_data(xls_url)

book = xlrd.open_workbook(file_contents=xls_data)
sheet = book.sheet_by_index(0)

title_row = 3
date_column = 0
vaccinations_column = 2

for row in range(title_row + 1, sheet.nrows):
    vd = sc.VaccinationData(canton='SZ', url=url)

    date = sheet.cell_value(row, date_column)
    date = datetime.datetime(*xlrd.xldate_as_tuple(date, book.datemode))
    vd.date = date.date().isoformat()

    vd.total_vaccinations = int(sheet.cell_value(row, vaccinations_column))

    assert vd
    print(vd)
