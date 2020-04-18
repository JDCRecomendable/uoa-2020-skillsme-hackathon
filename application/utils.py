#!/usr/bin/env python3

# -*- coding: utf-8 -*-

"""
Utilities
GreyHounds
2020 Skillsme Online Hackathon
Copyright (c) 2020 Jared Daniel Recomendable.

This program is free software; you may redistribute and/or modify it under the
terms of the GNU General Public License v3.0 as published by the Free Software
Foundation.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE.  See the GNU General Public License for more details.

PURPOSE
Provide various small-scale functions for the application.
"""

from datetime import datetime, date
from bs4 import BeautifulSoup
import requests


NZ_MOH_COV19_DETAILS_PAGE = "https://www.health.govt.nz/our-work/diseases-and-conditions/covid-19-novel-coronavirus/covid-19-current-situation/covid-19-current-cases/covid-19-current-cases-details"
NZ_MOH_DOMAIN = "https://www.health.govt.nz"


def date_to_string(date_obj):
    string = ""
    if type(date_obj) in (datetime, date):
        string += date_obj.strftime("%d/%m/%Y")
    elif type(date_obj) == str:
        string += date_obj
    return string


def retrieve_excel_urlpath():
    page = requests.get(NZ_MOH_COV19_DETAILS_PAGE)
    html = BeautifulSoup(page.text, "html.parser")
    for link in html.find_all("a", href=True):
        dir_link = link["href"]
        if dir_link[:7] == "/system":
            return NZ_MOH_DOMAIN + str(dir_link)


# DEBUG
if __name__ == "__main__":
    print(retrieve_excel_urlpath())