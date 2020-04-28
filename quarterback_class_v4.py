# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 11:56:24 2020

@author: Nate P
"""

import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
import re
from abbreviations import team_abbreviation_series as TAS
"""
Quarterback object that accepts player name as an argument and an optional pro-football-reference link. Object stores information relating to players career passing stats,
players current average salary, player contract year, and of course player name. Object will ONLY work on NFL Quarterbacks. Class set up used to conveniently store Quarterback
information in one place. 
"""
class Quarterback():
    """URL template for Pro Football Reference """
    pro_football_url = 'https://www.pro-football-reference.com/players/{}/{}00.htm'
    def __init__(self, name, fb_url = None):
        # IF/ELSE statement for optional pro-football-reference URL. 
        if fb_url is not None:
            self.pro_football_url = fb_url
        else:
            self.pro_football_url = self.pro_football_url.format(name.split()[1][0], name.split()[1][:4] + name.split()[0][:2])
        self.name = name
        # Scrape team name and stats at same time, so as not to make multiple requests. 
        self.qb_stats_team_name = self.qb_stats(self.scrape_qb_data_pro_football(self.name, self.pro_football_url))

        #Scrape function returns a tuple
        self.team_name = self.qb_stats_team_name[1]
        self.qb_stats = self.qb_stats_team_name[0]
        
        #
        self.contract_df = self.scrape_spotrac_data(self.name,self.team_name)
        
    def __str__(self):
        return '{} Quarterback Class'.format(self.name)
    def __repr__(self):
        return '{} Quarterback Class'.format(self.name)

    
    def scrape_qb_data_pro_football(self, name, url):
        """ Accepts a Quarterback name, URL. Returns a Beautiful Soup 'soup' object of the Quarterbacks career passing statistics"""
        # Pattern to account for players with 'II' after their name. Will match on fisrt name last name. 
        pattern = re.compile(r'\w+ \w+')
        # Scrape QB data. Return Soup
        qb_request = requests.get(url).text
        qb_soup = bs(qb_request, "lxml")
        if pattern.search(qb_soup.find('h1', {'itemprop':'name'}).text.strip().replace('.',''))[0] == name.replace('.',''):
            qb_soup = qb_soup
        else:
            url = url.replace('00','01')
            qb_request = requests.get(url).text
            qb_soup = bs(qb_request, "lxml")
            if pattern.search(qb_soup.find('h1', {'itemprop':'name'}).text.strip())[0]  == name:
                qb_soup = qb_soup
            else:
                url = url.replace('01','02')
                qb_request = requests.get(url).text
                qb_soup = bs(qb_request,'lxml')
        
        return qb_soup
    
    def qb_stats(self, soup):
        """ Accepts a Beautiful Soup 'soup' object. Returns a tuple of Pandas DataFrame object (of QB stats) and full team name as string """
        headers = [th.text for th in soup.findAll('tr')[0].findAll('th')]
        index = [th.text for th in soup.find('table').findAll('th')[32:len(soup.find('table').findAll('th'))]]
        index = [x.strip('+').strip('*') for x in index]
        stats = [[td.text for td in tr.findAll('td')] for tr in soup.find('table').findAll('tr')[1:len(soup.find('table').findAll('tr'))]]
        
        qb_df = pd.DataFrame(stats, index = pd.Index(index, name = 'Year'),  columns = headers[1:len(headers)])
        if soup.find('span',{'itemprop':'affiliation'}):
            team_name = soup.find('span',{'itemprop':'affiliation'}).text
        else:
            team_name = qb_df.loc['2019','Tm']
            team_name = TAS[team_name]

            
        return qb_df, team_name
    def scrape_spotrac_data(self, name, team_name):
        """ Accepts a quarterback name and FULL team name (not an abbreviation). Returns a Pandas Dataframe with quarterback Salary, Contract Year, and Name """
        spotrac_url = 'https://www.spotrac.com/nfl/{}/{}'.format(team_name.lower().replace(' ','-'), name.lower().replace(' ','-'))
        spotrac_request = requests.get(spotrac_url).text
        spotrac_soup = bs(spotrac_request, features = 'lxml')
        
        def spotrac_average_salary(spotrac_soup):
            """Returns average salary for most recent contract. """
            average_salary = ''
            if spotrac_soup.find('table').find('span',{'class':'playerLabel'}):
                for td in spotrac_soup.find('table').findAll('td'):
                    if td.find('span',{'class':'playerLabel'}).text == 'Average Salary':
                        average_salary = td.find('span',{'class':'playerValue'}).text
            else:
                average_salary = spotrac_soup.find('tr').find('td',{'class':'salaryAmt result'})
            return int(average_salary.strip('$').replace(',',''))       
    
        def spotrac_contract_year(spotrac_soup):
            """Returns contract year, or year BEFORE signing new contract"""
            contract_year = 0
            contract_year = int(spotrac_soup.findAll('td', {'class':'salaryYear center'})[0].text)
            if contract_year == 2021:
                return contract_year - 2
            else:
                return contract_year - 1
        
        sal = spotrac_average_salary(spotrac_soup)
        contract_year = spotrac_contract_year(spotrac_soup)
        
        return pd.DataFrame(data = {'Salary':sal, 'Contract Year':contract_year}, index = pd.Index(data = [self.name], name = 'Player'))