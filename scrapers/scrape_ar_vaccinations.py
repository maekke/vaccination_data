#!/usr/bin/env python3

import arrow
import re
import scrape_common as sc


def parse_ar_date(date_str):
    return arrow.get(date_str, 'DD.MM.YYYY', locale='de').datetime.date()


url = 'https://www.ar.ch/verwaltung/departement-gesundheit-und-soziales/amt-fuer-gesundheit/informationsseite-coronavirus/'
d = sc.download(url)
d = d.replace('&nbsp;', ' ')
d = re.sub(r'</?strong>', r'', d)
d = re.sub(r'(\d+)\'(\d+)', r'\1\2', d)

vd = sc.VaccinationData(canton='AR', url=url)

res = re.search(r'Impfzahlen.*Stand (\d+\.\d+\.\d{4})', d)
assert res
date = res[1]
date = parse_ar_date(date)

vd.date = date.isoformat()
res = re.search(r'>Bereits gelieferte Impfdosen: (\d+)', d)
assert res
vd.doses_delivered = res[1]

res = re.search(r'>Bereits verimpfte Impfdosen: (\d+)', d)
assert res
vd.total_vaccinations = res[1]
print(vd)
