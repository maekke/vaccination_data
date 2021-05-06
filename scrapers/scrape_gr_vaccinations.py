#!/usr/bin/env python3

import re
import arrow
from bs4 import BeautifulSoup
import scrape_common as sc


def parse_gr_date(date_str):
    return arrow.get(date_str, 'DD.MM.YYYY', locale='de').datetime.date()


url = 'https://www.gr.ch/DE/institutionen/verwaltung/djsg/ga/coronavirus/info/impfen/Seiten/impfen.aspx'

hist_url = 'https://www.gr.ch/DE/institutionen/verwaltung/djsg/ga/coronavirus/_layouts/15/GenericDataFeed/feed.aspx?PageID=30&ID=g_dbea8372_ed27_48e8_b2c8_b1f7a9643675&FORMAT=JSONRAW'
d = sc.download_json(hist_url)
for data in d:
    vd = sc.VaccinationData(canton='GR', url=url)
    vd.date = parse_gr_date(data['Stand'])
    vd.first_doses = int(data['verimpft1'])
    vd.second_doses = int(data['verimpft2'])
    vd.total_vaccinations = vd.first_doses + vd.second_doses
    print(vd)
