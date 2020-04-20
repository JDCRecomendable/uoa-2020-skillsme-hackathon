#!/usr/bin/env python3

# -*- coding: utf-8 -*-

"""
Web Scraping Utility
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
Scrape the NZ Health Ministry website and/or Excel file for data on the CoVID-19
cases.
"""


import requests
from bs4 import BeautifulSoup
from openpyxl import load_workbook


class Website:
    def __init__(self, url):
        """Define website parameters."""
        self.url = url
        self.page = requests.get(self.url)
        self.html = BeautifulSoup(self.page.content, "html.parser")
    
    def get_html(self):
        """Retrieve the raw HTML data from the website."""
        return self.html


class Scraper:
    def __init__(self, website):
        """Get website parameters.
        
        :param website: Website object
        """
        self.website = website
        self.html = website.get_html()
        self.tables = []
    
    def get_tables(self):
        """Get tbody data from the website."""
        if not self.tables:
            self.tables = self.html.select("tbody")
        return self.tables
    
    def format_table(self, table, start_row=None, end_row=None, start_col=None,
                     end_col=None):
        """Return a list of the rows of the table.
        
        The returned list contains lists, each representing a row in the table.
        Each list contained within the returned list contains strings of the
        content of each cell in the corresponding row.
        
        :param table: Table to format
        :param int start_row: Lower-limit index for the table row
        :param int end_row: Upper-limit index for the table row
        :param int start_col: Lower-limit index for the table column
        :param int end_col: Upper-limit index for the table column
        :rtype: list
        """
        results = []
        for row in table.select("tr")[start_row:end_row]:
            details = []
            for cell in row.select("td")[start_col:end_col]:
                details.append(str(cell)[4:-5])
            results.append(details)
        return results


class ExcelReader:
    def __init__(self, filepath):
        """Get Excel workbook parameters.
        
        :param str filename: Path to Excel file
        """
        self.workbook = load_workbook(filename=filepath)
    
    def get_worksheet_by_name(self, worksheet_name):
        """Retrieve the Excel worksheet by its name.
        
        :param str worksheet_name: Name of Excel worksheet, a string
        """
        return self.workbook[worksheet_name]
    
    def format_table(self, worksheet, start_row=None, end_row=None,
                     start_col=None, end_col=None):
        """Return a list of the rows of the worksheet.
        The returned list contains lists, each representing a row in the table.
        Each list contained within the returned list contains strings of the
        content of each cell in the corresponding row.
        
        :param worksheet: Worksheet object to format
        :param int start_row: Lower-limit index for the table row
        :param int end_row: Upper-limit index for the table row
        :param int start_col: Lower-limit index for the table column
        :param int end_col: Upper-limit index for the table column
        :rtype: list
        """
        results = []
        for row in worksheet.rows:
            details = []
            for cell in row:
                details.append(cell.value)
            results.append(details[start_col:end_col])
        return results[start_row:end_row]


class Covid19CasesListingWeb:
    def __init__(self, url):
        """Initialise the object.
        
        :param str url: URL to NZ Health Ministry Website.
        """
        self.url = url
        self.website = Website(self.url)
        self.scraper = Scraper(self.website)
    
    def _get_cases_table(self, i):
        return self.scraper.get_tables()[i]
    
    def get_cases(self, case_type=2):
        """Return a list of cases.
        
        :param int case_type: 0 for confirmed only, 1 for probable only, 2 for
        combined
        :return: List containing lists showing confirmed case data
        """
        if case_type != 2:
            table = self.scraper.format_table(self._get_cases_table(case_type))
        else:
            confirmed = self.scraper.format_table(self._get_cases_table(0))
            probable = self.scraper.format_table(self._get_cases_table(1))
            table = confirmed + probable
        return table
    
    def get_confirmed_cases(self):
        """Return a list of the confirmed cases.
        
        :return: List containing lists showing confirmed case data
        """
        return self.get_cases(0)
    
    def get_probable_cases(self):
        """Return a list of the probable cases.
        
        :return: List containing lists showing probable case data
        """
        return self.get_cases(1)
    
    def get_stat_count(self, stat_index, case_type=2):
        """Return a dictionary that counts the number of cases for each status
        type. Recommended for use with categorical variables.
        
        :param int stat_index: the status index is defined as the nth column for
        table as shown in the NZ Health Ministry website. E.g. as of 2020-04-14
        status index 1 refers to gender, status index 2 refers to age group, etc
        :param int case_type: 0 for confirmed only, 1 for probable only, 2 for
        combined
        :return: Dictionary whose keys is the region name and value is the count
        of cases for that region
        """
        results = {}
        cases = self.get_cases(case_type)
        for case in cases:
            if case[stat_index] not in results:
                results[case[stat_index]] = 1
            else:
                results[case[stat_index]] += 1
        return results
    
    def get_region_count(self, case_type=2):
        """Return a dictionary that counts the number of cases in each region.
        
        :param int case_type: 0 for confirmed only, 1 for probable only, 2 for
        combined
        :return: Dictionary whose keys is the region name and value is the count
        of cases for that region
        """
        return self.get_stat_count(3, case_type)
    
    def get_region_count_confirmed(self):
        """Return a dictionary that counts the number of confirmed cases in each
        region.
        
        :return: Dictionary whose keys is the region name and value is the count
        of cases for that region
        """
        return self.get_region_count(0)
    
    def get_region_count_probable(self):
        """Return a dictionary that counts the number of probable cases in each
        region.
        
        :return: Dictionary whose keys is the region name and value is the count
        of cases for that region
        """
        return self.get_region_count(1)


class Covid19CasesListingExcel(Covid19CasesListingWeb):
    def __init__(self, filepath, local_filepath=True):
        """Initialise the object.
        
        :param str filepath: Path to Excel workbook.
        :param bool local_filepath: True if the filepath given is on disk
        """
        self.filepath = filepath
        if local_filepath:
            r = requests.get(self.filepath)
            with open("cases.xlsx", mode="wb") as localfile:
                localfile.write(r.content)
            self.excel_reader = ExcelReader("cases.xlsx")
        else:
            self.excel_reader = ExcelReader(self.filepath)
    
    def _get_cases_table(self, i):
        if i == 0:
            return self.excel_reader.get_worksheet_by_name("Confirmed")
        else:
            return self.excel_reader.get_worksheet_by_name("Probable")
    
    def get_cases(self, case_type=2):
        """Return a list of cases.
        
        :param int case_type: 0 for confirmed only, 1 for probable only, 2 for
        combined
        :return: List containing lists showing confirmed case data
        """
        if case_type != 2:
            table = self.excel_reader.format_table(
                self._get_cases_table(case_type),
                start_row=4
            )
        else:
            confirmed = self.excel_reader.format_table(
                self._get_cases_table(0),
                start_row=4
            )
            probable = self.excel_reader.format_table(
                self._get_cases_table(1),
                start_row=4
            )
            table = confirmed + probable
        return table


if __name__ == "__main__":
    # WHAT IS THIS FOR?
    # Test if the files work here.
    
    url = "https://www.health.govt.nz/our-work/diseases-and-conditions/covid-19-novel-coronavirus/covid-19-current-situation/covid-19-current-cases/covid-19-current-cases-details"
    # excel_filepath = "https://www.health.govt.nz/system/files/documents/pages/covidcase_list_18_april_2020.xlsx" # Please download the latest Excel file from 
    excel_filepath = "https://www.health.govt.nz/system/files/documents/pages/web-covid-confprob_20200418-2.xlsx"
    # https://www.health.govt.nz/our-work/diseases-and-conditions/covid-19-novel-coronavirus/covid-19-current-situation/covid-19-current-cases/covid-19-current-cases-details
    
    covid19 = Covid19CasesListingExcel(excel_filepath)
    formatted = covid19.get_confirmed_cases()
    
    for line in formatted[:10]:
        print(line)
    
    # print()
    # print()
    # print(covid19.get_region_count(2))
    # print()
    # print(covid19.get_region_count_confirmed())
    # print()
    # print(covid19.get_region_count_probable())
    # print()
    # print(covid19.get_stat_count(5))
    # print()
    # print(covid19.get_stat_count(1))
    # print()
    print(covid19.get_stat_count(2))
    # print(formatted)
    # print("\n\n\n\n")
    # print(type(formatted))
