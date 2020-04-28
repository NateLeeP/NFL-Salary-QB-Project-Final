# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 11:44:03 2020

@author: Nate P
"""

import pandas as pd
import requests 
from bs4 import BeautifulSoup as bs

# Using pro-football reference, scrape passing statistics for every player who threw at least one pass in 2019.
nfl_stats_request = requests.get('https://www.pro-football-reference.com/years/2019/passing.htm').text
nfl_stats_soup = bs(nfl_stats_request, features = 'lxml')

nfl_stats_header = [th.text for th in nfl_stats_soup.find('tr')('th')]
nfl_stats_data = [[td.text for td in tr.findAll('td')] for tr in nfl_stats_soup.findAll('tr')[1:len(nfl_stats_soup.findAll('tr'))]]

# Create a pandas DataFrame from scraped passing data. 
nfl_raw_stats_df = pd.DataFrame(nfl_stats_data, columns = nfl_stats_header[1:])
# Save pandas DataFrame to csv. Will clean data in a separate file. 
nfl_raw_stats_df.to_csv('nfl_raw_stats_data_2019.csv',index = False)




# Using pro-football reference, scrape passing statistics for every player who threw at least one pass in 2018.
nfl_stats_request = requests.get('https://www.pro-football-reference.com/years/2018/passing.htm').text
nfl_stats_soup = bs(nfl_stats_request, features = 'lxml')

nfl_stats_header = [th.text for th in nfl_stats_soup.find('tr')('th')]
nfl_stats_data = [[td.text for td in tr.findAll('td')] for tr in nfl_stats_soup.findAll('tr')[1:len(nfl_stats_soup.findAll('tr'))]]

# Create a pandas DataFrame from scraped passing data. 
nfl_raw_stats_df = pd.DataFrame(nfl_stats_data, columns = nfl_stats_header[1:])
# Save pandas DataFrame to csv. Will clean data in a separate file. 
nfl_raw_stats_df.to_csv('nfl_raw_stats_data_2018.csv',index = False)






