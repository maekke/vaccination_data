#!/usr/bin/env python3

import re
import arrow
import scrape_common as sc


def parse_ai_date(date_str):
    return arrow.get(date_str, 'DD. MMMM YYYY', locale='de').datetime.date()


url = 'https://www.ai.ch/themen/gesundheit-alter-und-soziales/gesundheitsfoerderung-und-praevention/uebertragbare-krankheiten/coronavirus/impfung'
d = sc.download(url)
d = re.sub(r'(\d+)\'(\d+)', r'\1\2', d)

vd = sc.VaccinationData(canton='AI', url=url)

res = re.search(r'>Stand\s(.*\s\d{4}),\s\d+\sUhr<', d)
assert res
date = res[1]
date = parse_ai_date(date)
vd.date = date.isoformat()

res = re.search(r'<li>([0-9]+)\s+Personen geimpft \(kumuliert\)<\/li>', d)
assert res
vd.total_vaccinations = res[1]

assert vd
print(vd)
