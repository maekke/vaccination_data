#!/usr/bin/env python3

import re
import arrow
from bs4 import BeautifulSoup
import scrape_common as sc


def parse_ur_date(date_str):
    return arrow.get(date_str, 'D. MMMM YYYY', locale='de').datetime.date()


base_url = 'https://www.ur.ch'
main_url = f'{base_url}/themen/2962'
main_url = f'{base_url}/news.rss'
d = sc.download(base_url)
soup = BeautifulSoup(d, 'html.parser')

link = soup.find('a', text=re.compile('Lagebulletin '))

url = f"{base_url}{link.get('href')}"
d = sc.download(url)
d = re.sub(r'(\d+)\'(\d+)', r'\1\2', d)
d = re.sub(r'(\d+)’(\d+)', r'\1\2', d)
soup = BeautifulSoup(d, 'html.parser')

vd = sc.VaccinationData(canton='UR', url=url)

date_re = r'(\d+\. \w+ \d{4})'
item = soup.find('div', text=re.compile(date_re))
assert item
res = re.search(date_re, item.text)
assert res
vd.date = parse_ur_date(res[1])

ur_re = r'im Kanton Uri (rund )?(\d+) (Impfungen|Personen)'
content = None
element = soup.find('h3', text=re.compile('Impf|geimpft'))
if element:
    content = element.find_next('p').text
if not content:
    element = soup.find(string=re.compile(ur_re))
    assert element
    content = element.string
res = re.search(ur_re, content)
if res:
    vd.total_vaccinations = int(res[2])

    res = re.search(r'(\d+) Personen haben bereits die zweite Impfung erhalten', content)
    if not res:
        res = re.search(r'(\d+) Urnerinnen und Urner erhielten bereits (die|ihre) zweite Impfdosis', content)
    if res:
        vd.second_doses = int(res[1])
        vd.first_doses = vd.total_vaccinations - vd.second_doses

assert vd
print(vd)
