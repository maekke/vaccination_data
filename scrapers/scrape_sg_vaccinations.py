#!/usr/bin/env python3

import re
import arrow
import scrape_common as sc


def parse_sg_date(date_str):
    return arrow.get(date_str, 'D.MM.YYYY', locale='de').datetime.date()


main_url = 'https://www.sg.ch/ueber-den-kanton-st-gallen/statistik/covid-19.html'
url = 'https://stada.sg.ch/covid/Durchimpfung_SG.html'
url = 'https://stada.sg.ch/covid/BAG_Impfen_Zeitreihe_absolut.html'
d = sc.download(url)
d = re.sub(r'<br>', '', d)

# Datum:   2.08.2021 Total geimpfte Personen:  260448 davon einmal geimpft:  42011 davon zweimal geimpft:  218437"
for item in re.findall(r'"Datum:\s+(\d+\.\d+\.\d{4})\s+Total geimpfte Personen:\s+(\d+)\s+davon einmal geimpft:\s+(\d+)\s+davon zweimal geimpft:\s+(\d+)"', d):
    vd = sc.VaccinationData(canton='SG', url=main_url)
    vd.date = parse_sg_date(item[0])
    vd.total_vaccinations = int(item[1])
    vd.first_doses  = int(item[2])
    vd.second_doses = int(item[3])
    print(vd)
