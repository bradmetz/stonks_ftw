#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 20:46:13 2019

@author: Brad Metz
"""
# I am formating this file in blocks for each type collector i tried and used
# I am trying a number of of different ways of pulling, formatting and writing 
# I have also kept the methods that did not completely work with notes to 
# remember what happened.

# test of pandas_datareader class to pull down ticker data from Alpha Vantage
# this works nicely for less than 500 queries a day

import os
from datetime import datetime
import pandas_datareader.data as web

f = web.DataReader("TSE:T", "av-daily", start=datetime(2019, 10, 1), 
                   end=datetime(2019, 10, 22),
                   api_key=<<insert your key>>)
# test print entry
f.loc["2019-10-18"]

# web scraper to pull down all dividend stock tickers on the TSX from dividendhistory.org
# pull down the page in response
# this was a good exercise in using a combo of urllib and HTMLParser
# got the right parts of the table and regexes working
# was not able to prperly write out csv ... then found pandas HTML method call

import urllib.request
import numpy as np
import pandas as pd
import csv
#get page
response = urllib.request.urlopen('https://dividendhistory.org/tsx')
page_data = response.read()
# HTML Parse to get fields
from html.parser import HTMLParser
import re

class MyPageParser(HTMLParser):
    process_info = False
    tick_var = ''
    div_var = ''
    last_div_date = ''
    comp_name_var = ''
    df  = pd.DataFrame(columns=['tick_var', 'div_var', 'last_div_date', 'comp_name_var'])
    
    '''
    with open('stock_divs_tsx.csv', mode='w') as csv_file:
        fieldnames = ['ticker', 'dividend', 'last_div_date', 'company']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
    '''
    
    def handle_starttag(self, tag, attrs):
        if tag=='a':
            # can pull tickers from a tag with pattern payout/tsx/<symbol>
            attrs_str = str(attrs)
            #print(attrs_str)
            if ("/payout/tsx/" in attrs_str and "\\\\" in attrs_str):
            
                start_tok = '/payout/tsx/'
                end_tok = '\\\\'
                tick_sym = attrs_str[attrs_str.find(start_tok)+len(start_tok):attrs_str.rfind(end_tok)]
                print("here is what i want:", tick_sym)
                # found start pattern tick symbol
                # flag used to indicate follow on processing
                self.process_info = True
            else:
                self.process_info = False
    
    def handle_endtag(self, tag):
        if tag=='html':
            self.df.to_csv('./tickers_dividends_tsx.csv')
            print('found end of doc')
            
    def handle_data(self, data):
        #create a data frame and add fields until \n 
        # or just write out to csv with ticker in start tag
        #if process_info is True:
        if self.process_info is True:
            
            if(str(data).isupper()):
                print("this data matched ticker pattern", data)
                self.tick_var = str(data)
            elif(re.match('[0-9].{3,}(%)', str(data))):
                print("this data matched div rate pattern", data)
                self.div_var = str(data)
            elif(re.match('\d+-\d+-\d+', str(data))):
                print("this data matched date pattern", data)
                self.last_div_date = str(data)
            elif(re.match('[0-9A-Za-z.()-]{5}', str(data))):
                print('matched company name', data)
                self.comp_name_var = str(data)
            else:
                print("this data is left over assume end of record", str(data))
                print('\n')
                line = {'ticker':self.tick_var, 'dividend': self.div_var, 
                        'last_div_date': self.last_div_date, 'company':self.comp_name_var}
                
                '''with open('stock_divs_tsx.csv', mode='a') as csv_file:
                    #fieldnames = ['ticker', 'dividend', 'last_div_date', 'company']
                    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                    self.writer.writerow(line)'''
                self.df.append(line, ignore_index=True)
                print(line)
                self.process_info = False
                self.tick_var = ''
                self.div_var = ''
                self.last_div_date = ''
                self.comp_name_var = ''

# run page gathered with urllib through my custom parser
parser = MyPageParser()
parser.feed(str(page_data))

# so after fighting with building an HTML parser to extact the TSX dividend 
# from dividendhsitory.org, i found the method in pandas to pull down an
# HTML doc and parse all the tables into pandas data frames
# for this page the dataframe i want is the first (so index 0)
# the rest can be discarded 

import pandas as pd
dfs = pd.read_html('https://dividendhistory.org/tsx')
df = dfs[0]
df.to_csv('./datasets/pandas_div_history_tsx.csv')

# repeat to pull down the NYSE dividend stock list

import pandas as pd
dfs = pd.read_html('https://dividendhistory.org/nyse')
df = dfs[0]
df.to_csv('./datasets/pandas_div_history_nyse.csv')

# repeat to pull down the Nasdaq stock list

import pandas as pd
dfs = pd.read_html('https://dividendhistory.org/nasdaq')
df = dfs[0]
df.to_csv('./datasets/pandas_div_history_nasdaq.csv')

# basic code to pulldown dividend history based on stock ticker symbol
# TODO - Loop it through all tickers from previous step to popluate all 
# dividend history data points.

import pandas as pd
dfs = pd.read_html('https://dividendhistory.org/payout/tsx/AW_UN/')
df = dfs[0]
# dropthe first two rows since they are unconfirmed
# drop the last column (i can calculate div increase percentages myself) 
dfout = df.iloc[2:, :-1]
df.iloc[2:, :-1].to_csv('./datasets/ind_div_history/pandas_div_history_AW_UN.csv')
