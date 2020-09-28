#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 19:54:22 2020

@author: brad
"""

import pandas as pd
import calendar, datetime, os, sys
import numpy as np
import yfinance as yf
from datetime import date
from datetime import timedelta
from dateutil.relativedelta import relativedelta, FR
import stonks_extract as se
import stonks_output as so
import stonks_utils as su


# Globals for use across operations

SUCCESS = 0
FAILURE = -1
MARKETS = ('tsx', 'nyse', 'nasdaq')

# update each price history document for each ticker based on last 
# date recorded up to yesteday 
# this function meant to be used to update the existing dataset built
# running get_ticker_price_history previously 

# lazy solution is to just run full history collect and 
# overwrite full csv files each night

# TO BE REFACTORED - add to stonks_flow
# should be migrated to a stonks_flow

'''
def update_ticker_price_records(in_tickers: list, in_file_path:str, in_market:str):
    
    # full path to be provided going forward
    data_file_path = in_file_path
    #data_file_path = data_file_path + 'price_history/' 
    
    # get last record date from file
    i=0
    printProgressBar(0, len(in_tickers), prefix = f'{in_market} Price History Progress:', suffix = 'Complete', length = 50)

    
    for curr_sym in in_tickers:
        i += 1
        df = pd.DataFrame()
        printProgressBar(i, len(in_tickers), prefix = f'{in_market} Price History Progress:', suffix = 'Complete', length = 50)
        curr_sym = curr_sym.replace('.', '-')
        
        # may not need this for file path
        if in_market == 'tsx':
            curr_sym = curr_sym + '.TO'
        
        # FIX FILE PATH
        try:
            dfs = pd.read_csv(f'{data_file_path}yahoo_price_history_{curr_sym}.csv', keep_default_na=False)
        except:
            pass
        
        # grab date of last update on from price file
        dfs['Date'] = pd.to_datetime(dfs['Date'])
        last_date = dfs['Date'].max() + relativedelta(days=1)
        
        
        
        # this section can be replaced iwth a call to get_ticker_price_history with 
        # specified rnage determined above
        curr_tick = yf.Ticker(curr_sym)
        
        if last_date < date.today():
            df = curr_tick.history(start=last_date, end=date.today(), auto_adjust=False)
        else:
            #print(f"no update for {curr_sym}")
            pass
        
        
        if df.empty is False:
            #print(f"getting {curr_tick}")
            df['symbol'] = curr_sym.replace('.TO', '')
            df['market'] = in_market
            df = df.reset_index()
            df['date_epoch'] = df.apply (lambda x: int(x['Date'].timestamp())*1000, axis=1)
            # append to existing file
            df.to_csv(f'{data_file_path}yahoo_price_history_{curr_sym}.csv', mode='a', index=False, header=False)
        else:
            pass
    return 0
'''


# generalize function to take a list of tickers instead of a pandas dataframe
# returns 0 on success -1 otherwise
# default time period is "max" 
# write all price histories to in_file_path/price_histories
# may need to rethink how i code the daily updater code
# use in_period = 'spec' with in_start and in_end dates to specify
# a time interval.  not specifying end defaults to yesterday
# all functions will overwrite any existing data files

# path given should be full path to price history files
# if directory does not exist it will make it

# TO BE REFACTORED - add to stonks_flow
# - add extractor code to stonks_extract to return df for given ticker
# - add flow to get all price histories from tickers list and save as csv locally

#def get_ticker_price_history(in_tickers: list, in_period:str, in_file_path:str, in_market:str, *args, **kwargs):
    
    # setup based on input parameters
    #data_file_path = in_file_path
    #data_file_path = data_file_path + 'price_history/'
    #make_dir(data_file_path)
    
#    if in_period == 'max':
#        print("got max")
#    
#    elif in_period == 'last_day':
#        print("got last_day")
#    
#    elif in_period == 'spec':
#        print('got spec')
#        start = kwargs.get('in_start')
#        end = kwargs.get('in_end')
#        if start!=None:
#            if end==None:
#                end = date.today() # use yesterday as enddate by default. enddate in yfinance in non-inclusive
#        else:
#            print('You need to provide a start date with spec')
#            return -1
             
#    else:
#        test = kwargs.get('test')
##        print(test)
#        print('Only \'max\', \'spec\',  and \'last_day\' supported as this time')
#        return -1
    
#    if in_market not in su.MARKETS: #!= 'TSX' and in_market != 'NYSE' and in_market != 'NASDAQ':
#        print('market must be one of TSX, NYSE, or NASDAQ')
#        return -1
    
   # i=0
    #printProgressBar(0, len(in_tickers), prefix = f'{in_market} Price History Progress:', suffix = 'Complete', length = 50)

    
   # for curr_sym in in_tickers:
    #    i += 1
     #   printProgressBar(i, len(in_tickers), prefix = f'{in_market} Price History Progress:', suffix = 'Complete', length = 50)
        
       # curr_sym = curr_sym.replace('.', '-')
       # if in_market == 'TSX':
       #     curr_sym = curr_sym + '.TO'
       # curr_tick = yf.Ticker(curr_sym)
       # if in_period == 'max' or in_period =='last_day':    
       #     df = curr_tick.history(period=in_period, auto_adjust=False)
       # else:
       #     df = curr_tick.history(start=start, end=end, auto_adjust=False)
       # if df.empty is False:
            #print(f"getting {curr_tick}")
       #     df['symbol'] = curr_sym.replace('.TO', '')
       #     df['market'] = in_market
       #     df = df.reset_index()
       #     df['date_epoch'] = df.apply (lambda x: int(x['Date'].timestamp())*1000, axis=1)
       #     df.to_csv(f'{data_file_path}yahoo_price_history_{curr_sym}.csv', index=False)
       # else:
       #     pass
    #return su.SUCCESS
        

# in_country is either CAN or USA
# TO REFACTOR - generalize for local store anywhere (from csv) and add to 
#    stonks_extract

def get_last_weekly_report_date(in_country, in_path):
    
    if in_country!='USA' and in_country!='CAN':
        print("in_country must be one of CAN or USA")
        return -1
    try: 
        dates = os.listdir(f'{in_path}{in_country}')
    except FileNotFoundError:
        print(f"Dir {in_path}{in_country} no found")
        return FAILURE
    dates = [item.lstrip(f'div_history_report-{in_country}-') for item in dates]
    dates = [item.rstrip('.csv') for item in dates]

    maxdate = max(dates)    
    maxdate = datetime.datetime.strptime(maxdate, '%Y-%m-%d')

    return maxdate
    


# TO REFACTOR - add to stonks_flow to create all dividend yield records 
#    using proper ETL mods

def get_all_div_yield_histories(in_tickers: list, in_market: str, in_data_path: str):
    i=0
    printProgressBar(0, len(in_tickers), prefix = f'{in_market} Yield History Progress:', suffix = 'Complete', length = 50)

    
    for curr_sym in in_tickers:
        i += 1
        printProgressBar(i, len(in_tickers), prefix = f'{in_market} Yield History Progress:', suffix = 'Complete', length = 50)
        #curr_sym = curr_sym.replace('.', '_')
        if not daily_yield_calc_history(in_market, in_data_path, curr_sym):
            pass
        else:
            print(f"Error calculating {in_market} {curr_sym}")
            
    return 0

# create daily yields based on daily price data set 
# write to "yields" directory in datasets under project
# calculate and write daily yields using last declared div 
# update after each new div

# for each file in market dir 

# TO REFACTOR - add to transform with DF input and output
# prereq - DH weekly report, yahoo_daily_prices


def daily_yield_calc_history(in_market: str, in_data_path: str, in_ticker):
    
    
    
    # read in dividend history,  read in price history, calculate and add daily yield
    # data structure : date, date_epoch, price, dividend, yield
    
    if in_market != 'tsx' and in_market != 'nyse' and in_market != 'nasdaq':
        print('Market must be one of tsx, nyse, nasdaq')
        return -1
    
    # grab divdidend history for ticker
    try:
        data_file_path = in_data_path
        temp_tick = in_ticker.replace('.', '_')
        #print(in_ticker)
        dfs = pd.read_csv(f'{data_file_path}{in_market}/DH_div_history_{temp_tick}.csv', keep_default_na=False)
        div_path = data_file_path + "yield_history/"
        make_dir(div_path)
    except:
        print(f"Could not find {data_file_path}{in_market}/DH_div_history_{temp_tick}.csv")
        return -1
    
    #print(dfs)
    
    try:
        if in_market == 'tsx':
            dfs3 = pd.read_csv(f'./datasets/weekly_divhistory_reports/CAN/div_history_report-CAN-2020-08-14.csv', keep_default_na=False)
        else:
            dfs3 = pd.read_csv(f'./datasets/weekly_divhistory_reports/USA/div_history_report-USA-2020-08-14.csv', keep_default_na=False)
        dfs3.drop(columns=["Name", "Price", "Yld", "Ex-Div", "PayRto", "PE", "PB", "Beta", "Mkt Cap", "WK%", "MO%", "2MO%", "3MO%", "6MO%", "1YR%", "report_date_epoch", "ex_div_epoch"], inplace=True)
    except:
        print(f'Could not find weekly report for {in_market}')
        return -1
    
    # grab price history for ticker
    
    try:
        if in_market == 'tsx':
            in_ticker_can = in_ticker.replace('.', '-')
            in_ticker_can = in_ticker_can + '.TO'
            dfs2 = pd.read_csv(f'{data_file_path}price_history/yahoo_price_history_{in_ticker_can}.csv')
        else:
            in_ticker_us = in_ticker.replace('.', '-')
            dfs2 = pd.read_csv(f'{data_file_path}price_history/yahoo_price_history_{in_ticker}.csv')
        
        #print(dfs2)
    except:
        print(f"{data_file_path}price_history/yahoo_price_history_{in_ticker}.csv")
        return -1
    #print(dfs2)
   
    # join datasets on date and fill dividends down 
    
    dfs.rename(columns={'Ex-Dividend Date':'Date'}, inplace=True)
    result = pd.merge(dfs, dfs2, on=['Date'], how='outer')
    result.sort_values(by='Date', inplace=True)
    result.fillna(method='ffill', inplace=True)
    result.drop(columns=['Open', 'High', 'Low', 'Dividends', 'symbol', 'market', 'date_epoch', 'Stock Splits'], inplace=True)
    
    try:
        # frequency factor
        freq = dfs3.loc[dfs3['Symbol'] == in_ticker]
        #print(freq)
        if freq.iloc[0]['div_freq'] == 'Q':
            yield_factor = 4
        elif freq.iloc[0]['div_freq'] == 'S':
            yield_factor = 2
        elif freq.iloc[0]['div_freq'] == 'M':
            yield_factor = 12
        elif freq.iloc[0]['div_freq'] == 'A':
            yield_factor = 1
        else:
            # ignoring U and - for now
            yield_factor = 0
    except:
        print("Error getting freq")
        return -1
    
    
    # yield calculation
    result['Daily Yield'] = yield_factor*result['Cash Amount']/result['Close']
    # remove historic price records with no div
    result = result[result['Daily Yield'].notna()]
    
    # write out yield history by exchange and ticker
    make_dir(f"{data_file_path}yield_history/")
    
    #print(f"Path to write out {data_file_path}yield_history/yield_history_{in_market}_{in_ticker}.csv")
    result.to_csv(f"{data_file_path}yield_history/yield_history_{in_market}_{in_ticker}.csv", index=0)
    
    return 0

    

# returns an array of datetime objects of all fridays from the year given 
# to the last Friday from the current day
# use in_year=2019 - this is used for dataset initialization

def all_fridays_from(in_year):
    
    temp_year = in_year #kwargs.get('in_year')
    #pdate_flag = kwargs.get('update')
    #in_market = kwargs.get('in_market')
    #print(f"in_year: {temp_year}  update: {update_flag}  in_market: {in_market}")
    fridays = []
    if temp_year!=None and temp_year>2018:
        current_date = datetime.datetime.now()
        for year in range(temp_year, current_date.year+1):
            for month in range (1, 13):
                cal = calendar.monthcalendar(year, month)
                for week in cal:
                    if week[calendar.FRIDAY] != 0:
                        x = datetime.datetime(year, month, week[calendar.FRIDAY])
                        if x<current_date:
                            fridays.append(x.date())
    return fridays
   
# assumes that DH reports are stored with directories for each country
    
def fridays_since_last_DH_report(in_data_path, in_market):
    
    if in_market in ('nyse', 'nasdaq'):
        in_country = 'USA'
    elif in_market == 'tsx':
        in_country = 'CAN'
    else:
        print(f"{in_market} is not a valid market value")
        return FAILURE
    fridays = []
    
    temp_date = get_last_weekly_report_date(in_country, in_data_path)
    if temp_date == FAILURE:
        print(f"Error finding last report: {in_data_path} {in_market}")
        return FAILURE
    while temp_date<datetime.datetime.today():
        temp_date = next_weekday(temp_date, 4)
        if temp_date>datetime.datetime.today():
            break
        fridays.append(temp_date.date())
        
    return fridays

# helper function to test for Friday

def is_friday(in_date):
    if in_date.isoweekday() == 5:
        return SUCCESS
    return FAILURE

def next_weekday(d, weekday):
    days_ahead = weekday - d.weekday()
    if days_ahead <= 0: # Target day already happened this week
        days_ahead += 7
    return d + datetime.timedelta(days_ahead)

def get_last_friday():
    return date.today() + relativedelta(weekday=FR(-1))    

# assumes a date format YYYY-MM-DD 
def str_date_to_epoch(in_date_str):
    date_epoch = datetime.datetime.strptime(in_date_str, "%Y-%m-%d")
    return date_epoch.timestamp()

# returns 0 on success and -1 on error
def make_dir(path):
    if not os.path.exists(path):
        try:
            os.makedirs(path)
            print(f"Directory {path} created")
        except PermissionError:
            print(f"Permission to create directory {path} DENIED ... quitting.")
            return FAILURE
    return SUCCESS
        
# Print iterations progress
# taken from stack overflow: https://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()