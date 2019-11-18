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


''' ---------------------- ticker collector --------------------'''

# so after fighting with building an HTML parser ( code block below) to extact the TSX dividend 
# from dividendhsitory.org, i found the method in pandas to pull down an
# HTML doc and parse all the tables into pandas data frames
# for this page the dataframe i want is the first (so index 0)
# the rest can be discarded 

# use this section to initialize index for tickers and company names

import pandas as pd
dfs = pd.read_html('https://dividendhistory.org/tsx')
df = dfs[0]
#write out to csv for future use
df.to_csv('./datasets/pandas_div_history_tsx.csv')

# repeat to pull down the NYSE dividend stock list
dfs = pd.read_html('https://dividendhistory.org/nyse')
df = dfs[0]
df.to_csv('./datasets/pandas_div_history_nyse.csv')

dfs = pd.read_html('https://dividendhistory.org/nasdaq')
df = dfs[0]
df.to_csv('./datasets/pandas_div_history_nasdaq.csv')


''' --------------Code to write out records to elastic search --------------'''
# write out type to Elastic Index
'''
this section is used to push all tickers, company names, and next ex-dev to 
the Elastic search instance.  I used cURL to create the index (see readme)

    index - stonks_ftw
        type -  company
            ticker : string
            company name : string
            next_exdiv : date 
            market: string (one of TSX, NYSE, NASDAQ '''
            

# write all rows is dataframe as documents in companies index previously created
# this section performs TSX ticker import
    from datetime import datetime
    from elasticsearch import Elasticsearch
    import pandas as pd
    
    df = pd.read_csv('./datasets/pandas_div_history_tsx.csv', keep_default_na=False)
    for index, row in df.iterrows():
        #print(index, row)
        print('Symbol: {0} \n Company Name: {1} \n Next Ex-div: {2}'.format(row['Symbol'], row['Company'], row['Next Ex-div Date']))
        es = Elasticsearch("http://192.168.0.20:9200")
        es.info()
        es.index(index="stonks_ftw", doc_type="companies", body={"ticker":row['Symbol'], "company name":row['Company'], "next ex-div":row['Next Ex-div Date'], "market":"TSX"})

# this section performs NYSE ticker import
    from datetime import datetime
    from elasticsearch import Elasticsearch
    import pandas as pd
    
    df = pd.read_csv('./datasets/pandas_div_history_nyse.csv', keep_default_na=False)
    for index, row in df.iterrows():
        #print(index, row)
        print('Symbol: {0} \n Company Name: {1} \n Next Ex-div: {2}'.format(row['Symbol'], row['Company'], row['Next Ex-div Date']))
        es = Elasticsearch("http://192.168.0.20:9200")
        es.info()
        es.index(index="stonks_ftw", doc_type="companies", body={"ticker":row['Symbol'], "company name":row['Company'], "next ex-div":row['Next Ex-div Date'], "market":"NYSE"})

# this section performs NASDAQ ticker import
    from datetime import datetime
    from elasticsearch import Elasticsearch
    import pandas as pd
    
    df = pd.read_csv('./datasets/pandas_div_history_nasdaq.csv', keep_default_na=False)
    for index, row in df.iterrows():
        #print(index, row)
        print('Symbol: {0} \n Company Name: {1} \n Next Ex-div: {2}'.format(row['Symbol'], row['Company'], row['Next Ex-div Date']))
        es = Elasticsearch("http://192.168.0.20:9200")
        es.info()
        es.index(index="stonks_ftw", doc_type="companies", body={"ticker":row['Symbol'], "company name":row['Company'], "next ex-div":row['Next Ex-div Date'], "market":"NASDAQ"})





'''------------------------ Dividend history for each ticker----------------'''

# basic code to pulldown dividend history based on stock ticker symbol

import pandas as pd

# load tickers from previous summary csv
#tried loc with header 'Symbol'.  got errors finding Symbol
# not sure why but switched to integer index instead
# little quirk = kee_default_na needed to prevent the ticker value NA 
# from being converted into an nan
dfs = pd.read_csv('./datasets/pandas_div_history_tsx.csv', keep_default_na=False)
#ticks = dfs.loc[["Symbol"]]  -- getting errors on this
ticks = dfs.iloc[:, 1:2]
#list(ticks.columns.tolist())

##   print(col)

# loop throuigh all tickers and create new csv for each div stock

for (sym_index, sym_val) in ticks.iteritems():

    # learned i needed to go through a second loop to get at the string values for 
    # tickers so i can use them to create the individual stock page URLs
    
    #cycle through all tickers and pull down div history and store in data folder
    for sym in sym_val.values:
        sym = sym.replace('.', '_')
        print("https://dividendhistory.org/payout/tsx/{0}".format(sym))
        dfs = pd.read_html('https://dividendhistory.org/payout/tsx/{0}/'.format(sym))

# small decision block to deal with optional anoucements header on some pages
        if len(dfs)==3:
            df = dfs[0]
        elif len(dfs)==4:
            df = dfs[1]
        else:
            print('something else going on here')
# dropthe first two rows since they are unconfirmed
# drop the last column (i can calculate div increase percentages myself) 
        dfout = df.iloc[2:, :-1]
        df.iloc[2:, :-1].to_csv('./datasets/ind_div_history/tsx/pandas_div_history_{0}.csv'.format(sym))

# code to pull down nyse per ticker dividend history
# and save to nyse data directory 1 file per company

import pandas as pd

# load tickers from previous summary csv
#tried loc with header 'Symbol'.  got errors finding Symbol
# not sure why but switched to integer index instead
# little quirk = kee_default_na needed to prevent the ticker value NA 
# from being converted into an nan
dfs = pd.read_csv('./datasets/pandas_div_history_nyse.csv', keep_default_na=False)
#ticks = dfs.loc[["Symbol"]]  -- getting errors on this
ticks = dfs.iloc[:, 1:2]
#list(ticks.columns.tolist())

##   print(col)

# loop throuigh all tickers and create new csv for each div stock

for (sym_index, sym_val) in ticks.iteritems():

    #print("sym col", sym_index)
    #print("try one", sym_val.values[0])
    #print("sym_val", sym_val.values)
    # learned i needed to go through a second loop to get at the string values for 
    # tickers so i can use them to create the individual stock page URLs
    
    #cycle through all tickers and pull down div history and store in data folder
    for sym in sym_val.values:
        sym = sym.replace('.', '_')
        print("https://dividendhistory.org/payout/{0}".format(sym))
        dfs = pd.read_html('https://dividendhistory.org/payout/{0}/'.format(sym))

# small decision block to deal with optional anoucements header on some pages
        if len(dfs)==3:
            df = dfs[0]
        elif len(dfs)==4:
            df = dfs[1]
        else:
            print('something else going on here')
# dropthe first two rows since they are unconfirmed
# drop the last column (i can calculate div increase percentages myself) 
        dfout = df.iloc[2:, :-1]
        df.iloc[2:, :-1].to_csv('./datasets/ind_div_history/nyse/pandas_div_history_{0}.csv'.format(sym))

# code to pull down all nasdaq individual dividend history and save to 
# individual csv per company

import pandas as pd

# load tickers from previous summary csv
#tried loc with header 'Symbol'.  got errors finding Symbol
# not sure why but switched to integer index instead
# little quirk = kee_default_na needed to prevent the ticker value NA 
# from being converted into an nan
dfs = pd.read_csv('./datasets/pandas_div_history_nasdaq.csv', keep_default_na=False)
#ticks = dfs.loc[["Symbol"]]  -- getting errors on this
ticks = dfs.iloc[:, 1:2]
#list(ticks.columns.tolist())

##   print(col)

# loop throuigh all tickers and create new csv for each div stock

for (sym_index, sym_val) in ticks.iteritems():

    #print("sym col", sym_index)
    #print("try one", sym_val.values[0])
    #print("sym_val", sym_val.values)
    # learned i needed to go through a second loop to get at the string values for 
    # tickers so i can use them to create the individual stock page URLs
    
    #cycle through all tickers and pull down div history and store in data folder
    for sym in sym_val.values:
        sym = sym.replace('.', '_')
        print("https://dividendhistory.org/payout/{0}".format(sym))
        dfs = pd.read_html('https://dividendhistory.org/payout/{0}/'.format(sym))

# small decision block to deal with optional anoucements header on some pages
        if len(dfs)==3:
            df = dfs[0]
        elif len(dfs)==4:
            df = dfs[1]
        else:
            print('something else going on here')
# dropthe first two rows since they are unconfirmed
# drop the last column (i can calculate div increase percentages myself) 
        dfout = df.iloc[2:, :-1]
        df.iloc[2:, :-1].to_csv('./datasets/ind_div_history/nasdaq/pandas_div_history_{0}.csv'.format(sym))


'''------------------- Push Dividend history to Elastic instance ------------'''
''' index - stonks_ftw
        type -  company
            ticker : string
            company name : string
            next_exdiv : date
       
        type - div_history
            ticker : string
            exdiv_date : date
            payout_date : date
            amount : float
    
        type - price_history_with_yield
            ticker : string
            quote_date : date
            close_price : float
            div_yield : float

'''



import pandas as pd
import elasticsearch as es









# test of pandas_datareader class to pull down ticker data from Alpha Vantage
# this works nicely for less than 500 queries a day (may have to pull down
# bigger reports and parse offline to avoid hitting query ceiling)



from datetime import datetime
import pandas_datareader.data as web
import pandas as pd
import time 

# need to replace . with - in ticker symbols
# need to use outputsize=full to get full history
dfs = pd.read_csv('./datasets/pandas_div_history_tsx.csv', keep_default_na=False)
#ticks = dfs.loc[["Symbol"]]  -- getting errors on this
ticks = dfs.iloc[:, 1:2]
#list(ticks.columns.tolist())

##   print(col)

# loop throuigh all tickers and create new csv for each div stock

for (sym_index, sym_val) in ticks.iteritems():

    #cycle through all tickers and pull down div history and store in data folder
    # need to introduce a delay to respect 5 calls /minute limit
    # add error checking and retry if API catches too many tries
    
    for sym in sym_val.values:
        sym = sym.replace('.', '-')
        print("Alpha Vantage get CSV for: {0}".format(sym))
        df = pd.read_csv('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=TSE:{0}&apikey=U0W17L1FE65SS6LM&datatype=csv&outputsize=full'.format(sym))
        time.sleep(15)
        # add error checking for API violation here
        df.to_csv('./datasets/pricehistory/tsx/pandas_price_history_{0}.csv'.format(sym))
        


# experiment with web API call ... going with above since read_csv supports remote docs
# so i got excited to see the adjusted report provides dividend info ... 
# then got less excited when i realized that dividends do not show up for TSX stocks
# so still need to use and update my dividend index off of dividendhistory.org
        
f = web.DataReader("TSE:CTC-A", "av-daily-adjusted",
                   api_key='U0W17L1FE65SS6LM')

# web scraper to pull down all dividend stock tickers on the TSX from dividendhistory.org
# pull down the page in response
# this was a good exercise in using a combo of urllib and HTMLParser
# got the right parts of the table and regexes working
# was not able to prperly write out csv ... then found pandas HTML method call

import urllib.request
import pandas as pd
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


df = pd.read_csv('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=TSE:CTC-A&apikey=U0W17L1FE65SS6LM&outputsize=full')
        time.sleep(15)
        # add error checking for API violation here
        df.to_csv('./datasets/pricehistory/tsx/pandas_price_history_{0}.csv'.format(sym))