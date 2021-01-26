#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from bs4 import BeautifulSoup
import scrape_common as sc
from datetime import datetime

main_url = "https://www.baselland.ch/politik-und-behorden/direktionen/volkswirtschafts-und-gesundheitsdirektion/amt-fur-gesundheit/medizinische-dienste/kantonsarztlicher-dienst/aktuelles/covid-19-faelle-kanton-basel-landschaft/covid-19-impfungen"
main_site = sc.download(main_url)


def parse_row_date(s):
    row_date = s.replace('-', '.')
    parts = row_date.split('.')
    s_date = datetime(day=int(parts[0]), month=int(parts[1]), year=int(parts[2]))
    return s_date.date().isoformat()


def to_int(data):
    if data == '':
        return 0
    try:
        return int(float(data))
    except:
        return 0


soup = BeautifulSoup(main_site, 'html.parser')
for iframe in soup.find_all('iframe'):
    iframe_url = (iframe['src'])

    if iframe_url.find('/dbw/260') <= 0:
        continue

    d = sc.download(iframe_url)
    d = d.replace('\n', ' ')

    res = re.search(r'<pre id="data_1".*?> ?Datum,&quot;Mobiles Team&quot;,&quot;Impfzentrum Ost&quot;,&quot;Impfzentrum Mitte&quot;\s*([^<]+)</pre>', d)
    assert res
    data = res[1]
    if data:
        for row in data.split(" "):
            c = row.split(',')
            assert len(c) == 4, f"Number of fields changed, {len(c)} != 4"

            vd = sc.VaccinationData('BL', url=main_url)
            vd.date = parse_row_date(c[0])
            vd.total_vaccinations = to_int(c[1]) + to_int(c[2]) + to_int(c[3])
            print(vd)
        break
