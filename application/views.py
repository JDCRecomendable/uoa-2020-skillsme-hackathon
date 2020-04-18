#!/usr/bin/env python3

# -*- coding: utf-8 -*-

"""
Flask Views
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
Provide the front-end web views for the application.
"""

from application import app
from application.web_scraping import Covid19CasesListingExcel
from application.utils import date_to_string


@app.route("/")
def index():
    excel_filepath = "https://www.health.govt.nz/system/files/documents/pages/web-covid-confprob_20200418-2.xlsx"
    covid19 = Covid19CasesListingExcel(excel_filepath)
    formatted = covid19.get_confirmed_cases()
    text = ""
    for line in formatted:
        line[0] = date_to_string(line[0])
        text += str(line) + "<br>"
    return text
