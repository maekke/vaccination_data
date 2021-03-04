#!/usr/bin/env python3

import re
import json
import requests
import arrow
from bs4 import BeautifulSoup
import scrape_common as sc


def parse_ne_date(date_str):
    return arrow.get(date_str, 'YYYY-MM-DD', locale='de').datetime.date()


main_url = 'https://www.ne.ch/autorites/DFS/SCSP/medecin-cantonal/maladies-vaccinations/Pages/Covid-19-statistiques.aspx'
pdf_url = 'https://www.ne.ch/autorites/DFS/SCSP/medecin-cantonal/maladies-vaccinations/Documents/Covid-19-Statistiques/COVID19_PublicationInternet.pdf'
url = 'https://public.tableau.com/views/NeuchtelCOVID-19Vaccination/Vaccination?%3Aembed=y&%3AshowVizHome=no&%3Adisplay_count=y&%3Adisplay_static_image=y&%3AbootstrapWhenNotified=true&%3Alanguage=en&:embed=y&:showVizHome=n&:apiID=host0#navType=1&navSrc=Parse'

# inspired by
# https://stackoverflow.com/questions/62095206/how-to-scrape-a-public-tableau-dashboard

r = requests.get(
    url,
    params={
        ":embed": "y",
        ":showAppBanner": "false",
        ":showShareOptions": "true",
        ":display_count": "no",
        "showVizHome": "no"
    }
)
soup = BeautifulSoup(r.text, "html.parser")

tableauData = json.loads(soup.find("textarea", {"id": "tsConfigContainer"}).text)

dataUrl = f'https://public.tableau.com{tableauData["vizql_root"]}/bootstrapSession/sessions/{tableauData["sessionid"]}'

r = requests.post(dataUrl, data={
    "sheet_id": tableauData["sheetId"],
})

dataReg = re.search(r'\d+;({.*})\d+;({.*})', r.text, re.MULTILINE)
info = json.loads(dataReg.group(1))
data = json.loads(dataReg.group(2))

data = data["secondaryInfo"]["presModelMap"]["dataDictionary"]["presModelHolder"]["genDataDictionaryPresModel"]["dataSegments"]["0"]["dataColumns"]
vaccination_data = data[0]
vaccinations = vaccination_data['dataValues']
date_data = data[2]
dates = date_data['dataValues']

number_of_entries = len(dates)
first_doses = vaccinations[0:number_of_entries]

# second doses start at 2021-01-25
idx = dates.index('2021-01-25 00:00:00')
second_doses = vaccinations[number_of_entries:number_of_entries + idx + 1]
for i in range(number_of_entries - idx - 1):
    second_doses.append(0)


# data is in a strange ordering
# first the vaccinations per week newest to oldest
# afterwards the summed up (only vaccinations, not date).
# for now take the weekly ones and sum them up manually.
items = list(zip(first_doses, second_doses, dates))
items.reverse()

first_doses = 0
second_doses = 0
for item in items:
    vd = sc.VaccinationData(canton='NE', url=main_url)
    vd.date = parse_ne_date(item[2])
    first_doses += item[0]
    vd.first_doses = first_doses
    second_doses += item[1]
    vd.second_doses = second_doses
    vd.total_vaccinations = vd.first_doses + vd.second_doses
    assert vd
    print(vd)
