# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 11:58:14 2020

@author: Nate P
"""
"""
Import 'raw' scraped data and clean it using pandas. 

"""


import pandas as pd
import numpy as np

# Clean 2019 passing statistics
nfl_raw_stats_2019_df = pd.read_csv(r'nfl_raw_stats_data_2019.csv')

# Extracting every QB who played at least one game. Will use each QBs contract year to build training set on what QBs are paid on. 
# This prevents the discounting of QBs who did not play in 2019 (due to injury or otherwise)
nfl_stats_2019_df = nfl_raw_stats_2019_df[nfl_raw_stats_2019_df['G'] >= 1]
# Include only players listed as 'QB'
nfl_stats_2019_df = nfl_stats_2019_df[nfl_stats_2019_df['Pos'].isin(['QB','qb'])]

def wins_and_losses(row):
    """Function applied on DataFrame. Accepts a row, then using the 'QBrec' value in the row, inputs a value for three new columns: Wins, Losses, and Ties"""
    if row['Player'] == 'Taysom Hill':
        row['Wins'] = 0
        row['Losses'] = 0
        row['Ties'] = 0
        return row
    else:
        row['Wins'] = row['QBrec'].split('-')[0]
        row['Losses'] = row['QBrec'].split('-')[1]
        row['Ties'] = row['QBrec'].split('-')[2]
        return row
nfl_stats_2019_df = nfl_stats_2019_df.apply(wins_and_losses, axis = 1)

# Clean up player name. Remove '+' and '*'. These markings indicate Pro Bowl and All-Pro selections
nfl_stats_2019_df['Player'] = nfl_stats_2019_df['Player'].apply(lambda x: x.strip('+').strip('*'))

# Change 'NaN' to zero. Why? No QBR for any QB. NaN in 4QC (4th quarter comeback) and GWD (Game-winning Drive) means the QB had none
def clean_NaN(row):
    if np.isnan(row['QBR']):
        row['QBR'] = 0
    if np.isnan(row['4QC']):
        row['4QC'] = 0
    if np.isnan(row['GWD']):
        row['GWD'] = 0
    return row

nfl_stats_2019_df = nfl_stats_2019_df.apply(clean_NaN, axis = 1)

# Add year variable to distinguish between 2019 and 2018
nfl_stats_2019_df.insert(loc = 0, column = 'Year', value = [2019 for x in range(len(nfl_stats_2019_df))])



# Clean 2019 passing statistics
nfl_raw_stats_2018_df = pd.read_csv(r'nfl_raw_stats_data_2018.csv')

# Extracting every QB who played at least one game. Will use each QBs contract year to build training set on what QBs are paid on. 
# This prevents the discounting of QBs who did not play in 2019 (due to injury or otherwise)
nfl_stats_2018_df = nfl_raw_stats_2018_df[nfl_raw_stats_2018_df['G'] >= 1]
# Include only players listed as 'QB'
nfl_stats_2018_df = nfl_stats_2018_df[nfl_stats_2018_df['Pos'].isin(['QB','qb'])]
# 2018 Wins and Losses
nfl_stats_2018_df = nfl_stats_2018_df.apply(wins_and_losses, axis = 1)
# Clean up player name. Remove '+' and '*'. These markings indicate Pro Bowl and All-Pro selections
nfl_stats_2018_df['Player'] = nfl_stats_2018_df['Player'].apply(lambda x: x.strip('+').strip('*'))
# Change 'NaN' to zero. Why? No QBR for any QB. NaN in 4QC (4th quarter comeback) and GWD (Game-winning Drive) means the QB had none
nfl_stats_2018_df = nfl_stats_2018_df.apply(clean_NaN, axis = 1)

nfl_stats_2018_df.insert(loc =0, column = 'Year', value = [2018 for x in range(len(nfl_stats_2018_df))])

# Create QB Stats DataFrame that includes QBs who have thrown for 100 or more passes in either 2019 or 2018. Use most recent season of > 100 passes. 
# Remember: Crucial part of analysis will be player names that will be fed into loop. Using quarterback class to extract player personal data
nfl_stats_2019_df_100_passes = nfl_stats_2019_df[nfl_stats_2019_df['Att'] >= 100]
nfl_stats_2018_df_100_passes = nfl_stats_2018_df[nfl_stats_2018_df['Att'] >= 100]

nfl_stats_combined = pd.concat([nfl_stats_2019_df_100_passes, nfl_stats_2018_df_100_passes])
nfl_stats_combined = nfl_stats_combined.drop_duplicates(subset = 'Player').reset_index(drop = True)

# Save as CSV 2019 and 2018 passing stats. Will be using list of players to build out 'Contract Year' DF
nfl_stats_combined.to_csv(r'nfl_2019_2018_passing_stats.csv', index = False)


