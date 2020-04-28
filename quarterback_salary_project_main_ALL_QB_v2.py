# -*- coding: utf-8 -*-
"""
Created on Sat Apr  4 12:29:27 2020

@author: nlpru
"""

from quarterback_class_v3 import Quarterback
import pandas as pd



"""Script to read in starting quarterbacks from CSV. Create list of Quarterback objects. Proceed to create data set of each QBs contract year"""

# 2019 Stats and 2018 Stats for quarterback who threw AT LEAST ONE pass in 2018 or 2019. 
# Code below extracts players contract year, average salary. The DataFrame with 2018 and 2019 passing data is used to generate list of quarterbacks to scrape. 
nfl_stats_salary = pd.read_csv('nfl_2019_2018_passing_stats.csv')
qbs = list(nfl_stats_salary['Player'].values)

# Josh Allen and Daniel Jones had issues with their Pro Football Reference page that could be sorted out by passing a specific URL to Quarterback class
hot_fixes = {'Josh Allen':'https://www.pro-football-reference.com/players/A/AlleJo02.htm', 'Daniel Jones':'https://www.pro-football-reference.com/players/J/JoneDa05.htm'}

# Initializing an empty list to store 'Quarterback' objects
qbs_object_list = []

# Loop over list of quarterback names and add their corresponding 'Quarterback' object to the initalized object list. 
for name in qbs:
    if name in hot_fixes:
        qbs_object_list.append(Quarterback(name, hot_fixes[name]))
    else:
        try:
            qbs_object_list.append(Quarterback(name))
        except:
            print('{} did not work!'.format(name))

columns = [x.strip() for x in 'Age, Player, Tm, Pos, No., G, GS, QBrec, Cmp, Att, Cmp%, Yds, TD, TD%, Int, Int%, 1D, Lng, Y/A, AY/A, Y/C, Y/G, Rate, QBR, Sk, Yds, NY/A, ANY/A, Sk%, 4QC, GWD, AV, Salary'.split(',')]

# Empty DataFrame. This DataFrame will contain contract year stats and salary for veteran quarterbacks. 
d = pd.DataFrame(data = None, index = pd.Index(data = [], name = 'Year'), columns = columns)
# Empty DataFrame. This DataFrame will contain 2019 stats and salary for quarterbacks on their rookie deal. 
rookies = pd.DataFrame(data = None, index = pd.Index(data = [], name ='Year', columns = columns))

for qb in qbs_object_list:
    # Quarterback object contins 'Contract Year' stats, Career Stats, and Salary information.
    if str(qb.contract_df.loc[qb.name, 'Contract Year']) in list(qb.qb_stats.index):
        contract_year_df = qb.qb_stats.loc[[str(qb.contract_df.loc[qb.name, 'Contract Year'])]]
        contract_year_df.insert(loc = 1, column = 'Player', value = qb.name)
        contract_year_df.insert(loc = 32, column = 'Salary', value = qb.contract_df.loc[qb.name, 'Salary'])
        d = pd.concat([d, contract_year_df])
    else:
        print('{} is on his rookie deal'.format(qb.name))
        try:
            contract_year_df = qb.qb_stats.loc[['2019']]
            contract_year_df.insert(loc =1, column = 'Player', value = qb.name)
            contract_year_df.insert(loc = 32, column = 'Salary', value = qb.contract_df.loc[qb.name, 'Salary'])
        except:
            contract_year_df = qb.qb_stats.loc[['2018']]
            contract_year_df.insert(loc = 1, column = 'Player', value = qb.name)
            contract_year_df.insert(loc = 32, column = 'Salary', value = qb.contract_df.loc[qb.name, 'Salary'])

        rookies = pd.concat([rookies, contract_year_df])
        

# Load in 'quick fixes', veteran quarterbacks that did not work with Quarterback class. These quarterbacks needed to be handled differently due to issues with Spotrac.  
qb_quick_fixes = pd.read_csv(r'C:\Users\Nate P\Desktop\NFL Salary Project FINAL\qb_contracts_quick_fix.csv', index_col = 'Year')

# Change column names to match. 'd' column had 'Yds', not 'Yds.1'.
d.columns = qb_quick_fixes.columns
final_df = pd.concat([d, qb_quick_fixes])

final_df.to_csv('qb_contract_year_stats_df.csv')
rookies.to_csv('rookie_contracts_2019_stats.csv')





