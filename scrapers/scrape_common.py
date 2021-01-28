#!/usr/bin/env python3

import re
import subprocess
import requests


class VaccinationData:
    __initialized = False
    SEPARATOR = ','

    def __init__(self, canton=None, url=None):
        self.date = None
        self.week = None
        self.year = None
        self.canton = canton
        self.doses_delivered = None
        self.first_doses = None
        self.second_doses = None
        self.total_vaccinations = None
        self.url = url
        self.__initialized = True

    def __setattr__(self, key, value):
        if self.__initialized and not hasattr(self, key):
            raise TypeError(f'unknown key: {key}')
        object.__setattr__(self, key, value)

    def __str__(self):
        res = []
        res.append(self.canton)
        res.append('' if self.date is None else str(self.date))
        res.append('' if self.week is None else str(self.week))
        res.append('' if self.year is None else str(self.year))
        res.append('' if self.doses_delivered is None else str(self.doses_delivered))
        res.append('' if self.first_doses is None else str(self.first_doses))
        res.append('' if self.second_doses is None else str(self.second_doses))
        res.append('' if self.total_vaccinations is None else str(self.total_vaccinations))
        res.append(self.url)
        return VaccinationData.SEPARATOR.join(res)

    def __bool__(self):
        attributes = [
            self.doses_delivered,
            self.first_doses,
            self.second_doses,
            self.total_vaccinations,
        ]
        return any(v is not None for v in attributes)

    def parse(self, data):
        items = data.split(VaccinationData.SEPARATOR)
        if len(items) == 10:
            self.canton = items[0]
            self.date = items[1]
            self.week = self.__get_int_item(items[2])
            self.year = self.__get_int_item(items[3])
            self.doses_delivered = items[4]
            self.first_doses = items[5]
            self.second_doses = items[6]
            self.total_vaccinations = items[7]
            self.url = items[8]
            return True
        return False

    @staticmethod
    def __get_int_item(item):
        try:
            return int(item)
        except:
            return None

    @staticmethod
    def header():
        return 'canton,date,week,year,doses_delivered,first_doses,second_doses,total_vaccinations,source'


def _download(url, encoding='utf-8'):
    req = requests.get(url)
    req.raise_for_status()
    if encoding:
        req.encoding = encoding
    return req


def download(url, encoding='utf-8'):
    return _download(url, encoding).text


def download_data(url, encoding='utf-8'):
    return _download(url, encoding).content


def pdf_to_text(pdf, page=None, layout=False):
    #pdf_command = ['pdftotext', '-layout', path, '-']
    pdf_command = ['pdftotext', ]
    if page:
        pdf_command += ['-f', str(page), '-l', str(page)]
    if layout:
        pdf_command.append('-layout')
    pdf_command.append('-')
    pdf_command.append('-')
    p = subprocess.Popen(pdf_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    out = p.communicate(input=pdf)[0]
    return out.decode('utf-8')


def pdfinfo(pdf, attribute='Pages', encoding='utf-8'):
    pdf_command = ['pdfinfo', '-']
    p = subprocess.Popen(pdf_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    out = p.communicate(input=pdf)[0]
    out = out.decode(encoding)
    res = re.search(r'(\n|^)' + attribute + r':\s+(.*)(\n|$)', out)
    if res:
        return res[2]
    return None
