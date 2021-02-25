#!/usr/bin/env python3

import datetime
import xlrd
import scrape_common as sc


url = 'https://www.llv.li/inhalt/118804/amtsstellen/sonderseite-covid-19'
xls_url = 'https://www.llv.li/files/as/impfungen.xlsx'
xls_data = sc.download_data(xls_url)

book = xlrd.open_workbook(file_contents=xls_data)
sheet = book.sheet_by_index(0)

for i in range(1, 3):
    vd = sc.VaccinationData(canton='FL', url=xls_url)
    date = sheet.cell_value(3, i)
    date = datetime.datetime(*xlrd.xldate_as_tuple(date, book.datemode))
    vd.date = date.date().isoformat()
    vd.doses_delivered = int(sheet.cell_value(4, i))
    vd.total_vaccinations = int(sheet.cell_value(5, i))
    vd.second_doses = int(sheet.cell_value(6, i))
    vd.first_doses = vd.total_vaccinations - vd.second_doses

    assert vd
    print(vd)
