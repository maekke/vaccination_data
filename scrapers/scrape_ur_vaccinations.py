#!/usr/bin/env python3

import re
import arrow
from bs4 import BeautifulSoup
import scrape_common as sc


def parse_ur_date(date_str):
    return arrow.get(date_str, 'D. MMMM YYYY', locale='de').datetime.date()


base_url = 'https://www.ur.ch'
main_url = f'{base_url}/themen/2962'
d = sc.download(main_url)
soup = BeautifulSoup(d, 'html.parser')

links = soup.find_all('a', text=re.compile('Lagebulletin Sonderstab COVID-19 .*2021'))
for link in links:
    url = f"{base_url}{link.get('href')}"
    d = sc.download(url)
    d = re.sub(r'(\d+)\'(\d+)', r'\1\2', d)
    d = re.sub(r'(\d+)’(\d+)', r'\1\2', d)
    soup = BeautifulSoup(d, 'html.parser')

    vd = sc.VaccinationData(canton='UR', url=url)

    title = soup.find('h1', text=re.compile('Lagebulletin Sonderstab'))
    res = re.search(r'(\d+\. \w+ \d{4})', title.text)
    assert res
    vd.date = parse_ur_date(res[1])

    content = soup.find('h3', text=re.compile('Impf')).find_next('p').text
    res = re.search(r'im Kanton Uri (\d+) (Impfungen|Personen)', content)
    if res:
        vd.total_vaccinations = int(res[1])

        res = re.search(r'(\d+) Personen haben bereits die zweite Impfung erhalten', content)
        if res:
            vd.second_doses = int(res[1])
            vd.first_doses = vd.total_vaccinations - vd.second_doses

    if vd:
        print(vd)
