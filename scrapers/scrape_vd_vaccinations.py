#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import requests
import scrape_common as sc


main_url = 'https://monitoring.unisante.ch/d/krLTmEfGk/donnees-vaccination-covid-19-vaud'
url = 'https://monitoring.unisante.ch/api/tsdb/query'

from_date = int(datetime.datetime(year=2020, month=12, day=1).timestamp() * 1000)
to_date = int(datetime.datetime.today().timestamp() * 1000)

query = {"from": f"{from_date}","to": f"{to_date}","queries":[{"refId":"A","intervalMs":900000,"maxDataPoints":847,"datasourceId":11,"rawSql":"SELECT\r\n  count(hash) as \"Nombre de vaccinations - Première dose\",\r\n  date(first_vac_date) as time\r\nFROM monitoring_lines_public\r\nWHERE first_vac_date is not null and done_elsewhere_first = '0' and  $__timeFilter(first_vac_date)\r\nGROUP by date(first_vac_date)","format":"time_series"},{"refId":"B","intervalMs":900000,"maxDataPoints":847,"datasourceId":11,"rawSql":"SELECT\r\n  count(hash) as \"Nombre de vaccinations - Seconde dose\",\r\n  date(second_vac_date) as time\r\nFROM monitoring_lines_public\r\nWHERE second_vac_date is not null and done_elsewhere_second = '0' and  $__timeFilter(second_vac_date)\r\nGROUP by date(second_vac_date)","format":"time_series"}]}

req = requests.post(url, json=query)
data = req.json()

assert data['results']['A']['series'][0]['name'] == 'Nombre de vaccinations - Première dose'
assert data['results']['B']['series'][0]['name'] == 'Nombre de vaccinations - Seconde dose'
first_doses_data = data['results']['A']['series'][0]['points']
second_doses_data = data['results']['B']['series'][0]['points']

vaccination_data = {}

# daily data, needs summing up
first_doses = 0
for data in first_doses_data:
    date = datetime.date.fromtimestamp(data[1] / 1000)
    vd = sc.VaccinationData(canton='VD', url=main_url)
    vd.date = date.isoformat()
    first_doses += int(data[0])
    vd.first_doses = first_doses
    vd.total_vaccinations = first_doses
    vaccination_data[date] = vd

second_doses = 0
for data in second_doses_data:
    date = datetime.date.fromtimestamp(data[1] / 1000)
    if date not in vaccination_data:
        vd = sc.VaccinationData(canton='VD', url=main_url)
        vd.date = date.isoformat()
        vaccination_data[date] = vd
    vd = vaccination_data[date]
    second_doses += int(data[0])
    vd.second_doses = second_doses
    if vd.first_doses:
        vd.total_vaccinations = vd.first_doses + vd.second_doses

# first/second doses are not available on each day,
# add the missing ones with the last value
first_doses = None
second_doses = None
for date, vd in vaccination_data.items():
    if vd.first_doses:
        first_doses = vd.first_doses
    if vd.first_doses is None and first_doses:
        vd.first_doses = first_doses
    if vd.second_doses:
        second_doses = vd.second_doses
    if second_doses:
        vd.second_doses = second_doses
        vd.total_vaccinations = vd.first_doses + vd.second_doses
    print(vd)
