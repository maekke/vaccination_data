#!/usr/bin/env python3

import datetime
import re
from bs4 import BeautifulSoup
import scrape_common as sc


def parse_gr_date(date_str):
    date = datetime.date.fromtimestamp(date_str / 1000)
    return date.isoformat()


url = 'https://www.gr.ch/DE/institutionen/verwaltung/djsg/ga/coronavirus/info/impfen/Seiten/impfen.aspx'

json_url = 'https://services1.arcgis.com/YAuo6vcW85VPu7OE/arcgis/rest/services/Graub%C3%BCnden_Impfung_Final/FeatureServer/0/query?cacheHint=true&resultOffset=0&resultRecordCount=32000&where=1%3D1&orderByFields=Datum%20ASC&outFields=*&resultType=standard&returnGeometry=false&spatialRel=esriSpatialRelIntersects&f=pjson'
d = sc.download_json(json_url)
for feature in d['features']:
    data = feature['attributes']

    vd = sc.VaccinationData(canton='GR', url=url)
    vd.date = parse_gr_date(data['Datum'])
    vd.doses_delivered = int(data['Ausgelieferte_Impfdosen'])
    vd.total_vaccinations = int(data['Verabreichte_Impfdosen_Total'])
    print(vd)
