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
from application.web_scraping import Covid19CasesListingExcel, Covid19CasesListingWeb
import plotly.graph_objects as go
import plotly.express as px
import os
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

confirmed_or_probable = ['Confirmed Cases', 'Probable Cases']
def confirmed():

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

    gender_dict = covid19.get_stat_count(1)
    del gender_dict[None]
    gender_keys, gender_values = zip(*gender_dict.items()) 

    age_dict = {}
    for i in range(len(age_list)):
        age_dict[age_list[i]] = age_list.count(age_list[i])
    age_keys, age_values = zip(*age_dict.items()) 

    dhb_dict = covid19.get_region_count_confirmed()
    dhb_keys, dhb_values = zip(*dhb_dict.items()) 

    wentOverseas_dict = {}
    for i in range(len(wentOverseas_list)):
        wentOverseas_dict[wentOverseas_list[i]] = wentOverseas_list.count(wentOverseas_list[i])
    del wentOverseas_dict[' ']
    wentOverseas_keys, wentOverseas_values = zip(*wentOverseas_dict.items()) 

    chart_titles = ['Dates', 'Gender', 'Age', 'Region', 'Went Overseas']

    # Line chart function
    def line_chart(keys, values, cp, title):
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=keys,
            y=values,
            connectgaps = True
        ))

        fig.update_layout(
            title="Number of " + confirmed_or_probable[cp] + ' vs ' + chart_titles[title],
            yaxis_title=confirmed_or_probable[cp]+' cases',
            xaxis_title=chart_titles[title]
        )
        os.remove("Line chart of " + "Number of " + confirmed_or_probable[cp] + ' vs ' + chart_titles[title] + ".html")
        fig.write_html("Line chart of " + "Number of " + confirmed_or_probable[cp] + ' vs ' + chart_titles[title] + ".html")

    # Bar Chart Function
    def bar_chart(keys, values, cp, title):
        fig = go.Figure([go.Bar(
        x=keys, 
        y=values,  
        )])
        fig.update_layout(
            title="Number of " + confirmed_or_probable[cp] + ' vs ' + chart_titles[title],
            yaxis_title=confirmed_or_probable[cp]+' cases',
            xaxis_title=chart_titles[title]
        )

        os.remove("Bar chart of " + "Number of " + confirmed_or_probable[cp] + ' vs ' + chart_titles[title] + ".html")
        fig.write_html("Bar chart of " + "Number of " + confirmed_or_probable[cp] + ' vs ' + chart_titles[title] + ".html")

    # Pie Chart Function
    def pie_chart(keys, values, cp, title):
        labels = keys
        values = values

        fig = go.Figure(data=[go.Pie(title="Number of" + confirmed_or_probable[cp] + 'vs' + chart_titles[title], labels=labels, values=values,yaxis_title=confirmed_or_probable[cp]+'cases', xaxis_title=chart_titles[title])])
        fig.update_layout(
            title="Number of " + confirmed_or_probable[cp] + ' vs ' + chart_titles[title],
            yaxis_title=confirmed_or_probable[cp]+' cases',
            xaxis_title=chart_titles[title]
        )
        os.remove("Pie chart of " + "Number of " + confirmed_or_probable[cp] + ' vs ' + chart_titles[title] + ".html")
        fig.write_html("Pie chart of " + "Number of " + confirmed_or_probable[cp] + ' vs ' + chart_titles[title] + ".html")

    #NZ map


    # bar_chart(dates_keys, dates_values, 0, 0)
    # bar_chart(age_keys, age_values, 0, 2)
    # bar_chart(gender_keys, gender_values, 0, 1)
    # bar_chart(wentOverseas_keys, wentOverseas_values, 0, 4)
    # bar_chart(dhb_keys, dhb_values, 0, 3)



# print()
# print()