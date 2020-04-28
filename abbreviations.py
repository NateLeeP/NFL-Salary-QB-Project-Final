# -*- coding: utf-8 -*-
"""
Created on Mon Apr  6 23:35:02 2020

@author: nlpru
"""

""" In the Quarterback classes, team abbreviations must be converted to team names, i.e. SEA needs to convert to 'Seattle Seahawks'. 'abbreviations.py' scrapes the abbreviations
from predictem.com, then stores the 'abbrevation: Team Name' pair into a Series, with the abbreviation as the index. 'team_abbreviation_series' is then imported into 'quarterback_class' """

import requests 
from bs4 import BeautifulSoup as bs
import pandas as pd
abbreviations_url = 'https://www.predictem.com/nfl/nfl-football-acronyms-abbreviations/'
abbreviations_request = requests.get(abbreviations_url).text
abbreviations_soup = bs(abbreviations_request, 'lxml')
team_abbreviation = []
team_full_name = []

for a in abbreviations_soup.findAll('p')[3].findAll('strong'):
    team_abbreviation.append(a.text)
    team_full_name.append(a.next_sibling.strip(':').strip(' '))

team_abbreviation_series = pd.Series(team_full_name, index = team_abbreviation)
#Rename to match Pro Football Reference conventions
team_abbreviation_series = team_abbreviation_series.rename(index = {'TB':'TAM'})