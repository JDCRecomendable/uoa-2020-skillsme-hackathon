#!/usr/bin/env python3

# -*- coding: utf-8 -*-

"""
INSERT TITLE HERE
GreyHounds
2020 Skillsme Online Hackathon
Sebastian Thomas

This program is free software; you may redistribute and/or modify it under the
terms of the GNU General Public License v3.0 as published by the Free Software
Foundation.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE.  See the GNU General Public License for more details.
"""

from application.utils import retrieve_excel_urlpath
from application.web_scraping import Covid19CasesListingExcel
# import plotly.graph_objects as go
from datetime import datetime


# Retrieve the link to the correct excel file
# res = requests.get('https://www.health.govt.nz/our-work/diseases-and-conditions/covid-19-novel-coronavirus/covid-19-current-situation/covid-19-current-cases/covid-19-current-cases-details')
# soup = bs4.BeautifulSoup(res.text, 'html.parser')
# for link in soup.find_all('a', href = True):
#     x = link['href']
#     if x[:7] == '/system':
#         data = 'https://www.health.govt.nz' + str(x)
#     else:
#         pass
data = retrieve_excel_urlpath()

url = "https://www.health.govt.nz/our-work/diseases-and-conditions/covid-19-novel-coronavirus/covid-19-current-situation/covid-19-current-cases/covid-19-current-cases-details"
excel_filepath = data # Please download the latest Excel file from 
# https://www.health.govt.nz/our-work/diseases-and-conditions/covid-19-novel-coronavirus/covid-19-current-situation/covid-19-current-cases/covid-19-current-cases-details

covid19 = Covid19CasesListingExcel(excel_filepath)
formatted = covid19.get_confirmed_cases()


dates_list = []
gender_list = []
age_list = []
dhb_list = []
wentOverseas_list = []

for line in formatted:
    dates_list.append(line[0])
    dates_list.sort(key = lambda date: datetime.strptime(date, '%d/%m/%Y'))
    gender_list.append(line[1])
    age_list.append(line[2])
    dhb_list.append(line[3])
    wentOverseas_list.append(line[4])

dates_dict = {}
for i in range(len(dates_list)):
    dates_dict[dates_list[i]] = dates_list.count(dates_list[i])
dates_keys, dates_values = zip(*dates_dict.items()) 

gender_dict = {}
for i in range(len(gender_list)):
    gender_dict[gender_list[i]] = dates_list.count(gender_list[i])

age_dict = {}
for i in range(len(age_list)):
    age_dict[age_list[i]] = age_list.count(age_list[i])

dhb_dict = {}
for i in range(len(dates_list)):
    dhb_dict[age_list[i]] = dhb_list.count(dhb_list[i])

wentOverseas_dict = {}
for i in range(len(wentOverseas_list)):
    wentOverseas_dict[wentOverseas_list[i]] = wentOverseas_list.count(wentOverseas_list[i])

# Line chart for Date vs no. of confirmed deaths
# fig1 = go.Figure()

# fig1.add_trace(go.Scatter(
#     x=dates_keys,
#     y=dates_values,
#     connectgaps = True
# ))

# fig1.show()

# Bar chart for Date vs no. of confirmed deaths
# fig = go.Figure([go.Bar(x=dates_keys, y=dates_values)])
# fig.show()




# print()
# print()