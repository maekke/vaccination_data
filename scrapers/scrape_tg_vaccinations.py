#!/usr/bin/env python3

import csv
import arrow
from io import StringIO
import scrape_common as sc


def parse_tg_date(date_str):
    return arrow.get(date_str, 'DD.MM.YYYY', locale='de').datetime.date()


def get_value(row, key):
    value = row[key]
    if value != '':
        return int(value)
    return None


url = 'https://statistik.tg.ch/public/upload/assets/94501/COVID19_Fallzahlen_Kanton_TG.csv'
d_csv = sc.download(url)

reader = csv.DictReader(StringIO(d_csv), delimiter=';')
total_doses_delivered = 0
for row in reader:
    if not row['date']:
        continue
    vd = sc.VaccinationData(canton='TG', url=row['source'])
    date = row['date']
    date = parse_tg_date(date)
    vd.date = date.isoformat()
    vd.total_vaccinations = get_value(row, 'total_vaccinations')
    doses_delivered = get_value(row, 'doses_delivered')
    if doses_delivered:
        total_doses_delivered += doses_delivered
        vd.doses_delivered = total_doses_delivered
    vd.first_doses = get_value(row, 'first_doses')
    vd.second_doses = get_value(row, 'second_doses')
    if vd:
        print(vd)
