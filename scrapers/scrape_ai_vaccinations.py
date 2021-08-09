#!/usr/bin/env python3

import re
import arrow
import scrape_common as sc


def parse_ai_date(date_str):
    try:
        return arrow.get(date_str, 'D. MMMM YYYY', locale='de').datetime.date()
    except arrow.parser.ParserMatchError:
        return arrow.get(date_str, 'D. MMMMYYYY', locale='de').datetime.date()


url = 'https://www.ai.ch/themen/gesundheit-alter-und-soziales/gesundheitsfoerderung-und-praevention/uebertragbare-krankheiten/coronavirus/impfung'
d = sc.download(url)
d = re.sub(r'(\d+)\'(\d+)', r'\1\2', d)

vd = sc.VaccinationData(canton='AI', url=url)

res = re.search(r'>Stand\s(.*\s?\d{4}),\s\d+\sUhr<', d)
assert res
date = res[1]
date = parse_ai_date(date)
vd.date = date.isoformat()

res = re.search(r'1. Impfdosis:\s+(\d+)', d)
assert res
vd.first_doses = int(res[1])

res = re.search(r'2. Impfdosis:\s+(\d+)', d)
assert res
vd.second_doses = int(res[1])

vd.total_vaccinations = vd.first_doses + vd.second_doses

assert vd
print(vd)
