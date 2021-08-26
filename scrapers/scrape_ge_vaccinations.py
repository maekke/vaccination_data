#!/usr/bin/env python3

import datetime
import re
import arrow
import scrape_common as sc


def parse_ge_date(date_str):
    date = arrow.get(date_str, 'D MMMM YYYY', locale='fr')
    return datetime.date(year=2021, month=date.month, day=date.day).isoformat()


url = 'https://www.ge.ch/se-faire-vacciner-contre-covid-19/chiffres-campagne-vaccination-geneve#chiffres'
d = sc.download(url)
d = re.sub(r'(\d+)\'(\d+)', r'\1\2', d)
d = d.replace(u'\xa0', u' ')

vd = sc.VaccinationData(canton='GE', url=url)

tot_vacc_re = r'.*\s+(\d+)\s+doses ont .*'
res = re.search(tot_vacc_re, d)
assert res
vd.total_vaccinations = int(res[1])

date_re = r'<p>[Aa]u\s+(\d+\s+\w+\s+\d{4})'
res = re.search(date_re, d)
assert res
vd.date = parse_ge_date(res[1])

res = re.search(r'.*\s+(\d+)\s+personnes\s+ont\s+re.u\s+la\s+1.*', d)
assert res
vd.first_doses = int(res[1])

res = re.search(r'.*\s+(\d+)\s+personnes\s+ont\s+re.u\s+leur\s+2.*', d)
assert res
vd.second_doses = int(res[1])

assert vd
print(vd)
