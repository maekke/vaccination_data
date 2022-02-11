#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
from collections import OrderedDict
import requests
import scrape_common as sc


main_url = 'https://monitoring.unisante.ch/d/krLTmEfGk/donnees-vaccination-covid-19-vaud'
url = 'https://monitoring.unisante.ch/api/tsdb/query'

from_date = int(datetime.datetime(year=2020, month=12, day=1).timestamp() * 1000)
to_date = int(datetime.datetime.today().timestamp() * 1000)

query = {"from": f"{from_date}","to": f"{to_date}","queries":[{"refId":"A","intervalMs":600000,"maxDataPoints":1153,"datasourceId":11,"rawSql":"SELECT\r\ncount(*)as \"Nombre de vaccinations - Première dose\", \r\nday_dates.daydate as time\r\nFROM day_dates left join vaccination_monitoring_lines on day_dates.daydate = date_format(\r\n\t\t`vaccination_monitoring_lines`.`injection_date`,\r\n\t\t'%Y-%m-%d'\r\n\t)\r\nWHERE $__timeFilter(day_dates.daydate) and done_elsewhere = '0' and serie = 1 and dose_number = 1\r\nGROUP by day_dates.daydate\r\norder by day_dates.daydate","format":"time_series"},{"refId":"B","intervalMs":600000,"maxDataPoints":1153,"datasourceId":11,"rawSql":"SELECT\r\ncount(*)as \"Nombre de vaccinations - Deuxième dose\", \r\nday_dates.daydate as time\r\nFROM day_dates left join vaccination_monitoring_lines on day_dates.daydate = date_format(\r\n\t\t`vaccination_monitoring_lines`.`injection_date`,\r\n\t\t'%Y-%m-%d'\r\n\t)\r\nWHERE $__timeFilter(day_dates.daydate) and done_elsewhere = '0' and serie = 1 and dose_number = 2\r\nGROUP by day_dates.daydate\r\norder by day_dates.daydate","format":"time_series"},{"refId":"C","intervalMs":600000,"maxDataPoints":1153,"datasourceId":11,"rawSql":"SELECT\r\ncount(*)as \"Nombre de vaccinations - Troisième dose\", \r\nday_dates.daydate as time\r\nFROM day_dates left join vaccination_monitoring_lines on day_dates.daydate = date_format(\r\n\t\t`vaccination_monitoring_lines`.`injection_date`,\r\n\t\t'%Y-%m-%d'\r\n\t)\r\nWHERE $__timeFilter(day_dates.daydate) and done_elsewhere = '0' and serie = 1 and dose_number = 3\r\nGROUP by day_dates.daydate\r\norder by day_dates.daydate","format":"time_series"},{"refId":"D","intervalMs":600000,"maxDataPoints":1153,"datasourceId":11,"rawSql":"SELECT\r\nsum(case when injection_date is not null  then 1 else 0 end) as \"Nombre de vaccinations - Rappel\",\r\nday_dates.daydate as time \r\nFROM day_dates left join vaccination_monitoring_lines on day_dates.daydate = date_format(\r\n\t\t`vaccination_monitoring_lines`.`injection_date`,\r\n\t\t'%Y-%m-%d'\r\n\t)\r\nWHERE $__timeFilter(day_dates.daydate) AND vaccination_monitoring_lines.done_elsewhere <> '1' and dose_number = 1 and serie >= 2\r\nGROUP by day_dates.daydate","format":"time_series"}]}

req = requests.post(url, json=query)
data = req.json()

assert data['results']['A']['series'][0]['name'] == 'Nombre de vaccinations - Première dose'
assert data['results']['B']['series'][0]['name'] == 'Nombre de vaccinations - Deuxième dose'
assert data['results']['C']['series'][0]['name'] == 'Nombre de vaccinations - Troisième dose'
first_doses_data = data['results']['A']['series'][0]['points']
second_doses_data = data['results']['B']['series'][0]['points']
third_doses_data = data['results']['C']['series'][0]['points']

vaccination_data = {}

# daily data, needs summing up
first_doses = 0
for data in first_doses_data:
    date = datetime.date.fromtimestamp(data[1] / 1000)
    vd = sc.VaccinationData(canton='VD', url=main_url)
    vd.date = date.isoformat()
    first_doses += int(data[0])
    vd.first_doses = first_doses
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

third_doses = 0
for data in third_doses_data:
    date = datetime.date.fromtimestamp(data[1] / 1000)
    if date not in vaccination_data:
        vd = sc.VaccinationData(canton='VD', url=main_url)
        vd.date = date.isoformat()
        vaccination_data[date] = vd
    vd = vaccination_data[date]
    third_doses += int(data[0])
    vd.total_vaccinations = third_doses

ordered_vd = OrderedDict(sorted(vaccination_data.items()))

# first/second doses are not available on each day,
# add the missing ones with the last value
first_doses = None
second_doses = None
for date, vd in ordered_vd.items():
    if vd.first_doses:
        first_doses = vd.first_doses
    if vd.first_doses is None and first_doses:
        vd.first_doses = first_doses
    if vd.second_doses:
        second_doses = vd.second_doses
    if vd.second_doses is None and second_doses:
        vd.second_doses = second_doses
    if vd.total_vaccinations is None:
        vd.total_vaccinations = 0
    vd.total_vaccinations += vd.first_doses
    if second_doses:
        vd.total_vaccinations += second_doses

    assert vd
    print(vd)
