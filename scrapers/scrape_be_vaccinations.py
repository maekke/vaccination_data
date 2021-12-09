#!/usr/bin/env python3

import csv
import re
from io import StringIO
import arrow
import scrape_common as sc


def parse_be_date(date_str):
    return arrow.get(date_str).datetime.date()


url = 'https://covid-kennzahlen.apps.be.ch/#/de/cockpit'
csv_url = 'https://raw.githubusercontent.com/openDataBE/VacMeData/develop/vaccination_key_figures.csv'
d = sc.download(csv_url)

reader = csv.DictReader(StringIO(d), delimiter=',')
for row in reader:
    vd = sc.VaccinationData(canton='BE', url=url)
    date = row['dateStats']
    if date == '':
        continue
    vd.date = parse_be_date(date)
    # this is not really perfect (for example doesn't take J&J into account)
    vd.second_doses = int(row['baseImmunized'])
    vd.first_doses = vd.second_doses
    vd.total_vaccinations = vd.first_doses + vd.second_doses + int(row['personBoostered'])
    print(vd)
