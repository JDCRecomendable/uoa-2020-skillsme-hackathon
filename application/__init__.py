#!/usr/bin/env python3

# -*- coding: utf-8 -*-

"""
CoVID-19 Main Solution Python File
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
Entry point for the application.
"""

from flask import Flask
app = Flask(__name__)


import application.views
