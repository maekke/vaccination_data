#!/usr/bin/env python3

import collections
import csv
import arrow
from io import StringIO
import scrape_common as sc


def parse_zg_date(date_str):
    return arrow.get(date_str, 'DD.MM.YYYY', locale='de').datetime.date()


csv_url = 'https://www.zg.ch/behoerden/gesundheitsdirektion/statistikfachstelle/daten/themen/result-themen-14-03-12.csv'
d_csv = sc.download(csv_url)
"""
"Datum","Typ","Anzahl","Meta","Type","Content"
"23.12.2020","Total verimpfte Dosen","250",NA,NA,NA
"24.12.2020","Total verimpfte Dosen","250",NA,NA,NA
"""

reader = csv.DictReader(StringIO(d_csv), delimiter=',')
data = collections.defaultdict(dict)
for row in reader:
    if row['Datum'] == 'NA':
        continue
    date = parse_zg_date(row['Datum'])
    if date not in data:
        vd = sc.VaccinationData(canton='ZG', url=csv_url)
        vd.date = date.isoformat()
        data[date] = vd
    if row['Typ'] == 'Total verimpfte Dosen':
        data[date].total_vaccinations = row['Anzahl']
    elif row['Typ'] == 'Total 1. Impfung':
        data[date].first_doses = row['Anzahl']
    elif row['Typ'] == 'Total 2. Impfung':
        data[date].second_doses = row['Anzahl']

dates = list(data.keys())
for date in dates:
    print(data[date])
