#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Title: stonks_extract - Extraction module with functions to pull 
data from multiple sources (online and local) and output as 
pandas dataframe for further processing and analysis. 

Version 0.1
- initial decoupling of extraction code from stonks_utils
- support for dividendhistory.org data extraction for US and Canadian markets
- support for reading in dividendhistory.org datasets from local csv
    


"""

import pandas as pd
import datetime
from urllib.error import HTTPError
from datetime import date
import numpy as np
import yfinance as yf

import stonks_utils as su


# ------------------------ Remote Extractors DividendHistory-------------------------

# get summary of tickers from dividendhistory.org
# in_market is one of tsx, nyse, nasdaq
# adds exchange and epoch time stamp for next ex-div
# returns a dataframe with the following structure 
# Symbol, Company, Yield Percentage, Next Ex-div Date, Exchange, ex-div epoch


def get_ticker_summary_divhistory(in_market: str):
    
    if not (in_market in su.MARKETS):
        print('in_market must be one of tsx, nyse, nasdaq')
        return pd.DataFrame()
    
    try:
        dfs = pd.read_html(f'https://dividendhistory.org/{in_market}', keep_default_na=False, header=0, index_col=0)
    except HTTPError as err:
        print(f"Could not get TSX ticks: HTTP Code: {err.code}  Path Tried: {err.url}")
        return pd.DataFrame()
    df = dfs[0]
    df['Exchange'] = "TSX"
    df['ex-div epoch'] = df.apply (lambda x: int(((datetime.datetime.strptime(x['Next Ex-div Date'], "%Y-%m-%d")).timestamp())*1000), axis=1)
    return df

# returns ticker symbols in a list extracted from divhistory remotely

def get_tickers_divhistory(in_market: str):
    if not (in_market in su.MARKETS):
        print('in_market must be one of tsx, nyse, nasdaq')
        return su.FAILURE
    try:
        dfs = pd.read_html(f'https://dividendhistory.org/{in_market}', keep_default_na=False)
    except HTTPError as err:
        print(f"Could not get {in_market} ticks: HTTP Code: {err.code}  Path Tried: {err.url}")
        return su.FAILURE
    df = dfs[0]
    sym_list = df['Symbol'].to_list()
    return (sym_list)

# get dividend history from dividendhistory.org for given ticker symbol
# returns DataFrame

def get_div_history_DH(in_sym, in_market):
    
    # extract module for pulling dividend history given ticker
    if not is_in_exchange_DH(in_sym, in_market):
        print(f"{in_sym} is not in {in_market} on dividendhistory")
        return pd.DataFrame()
    
    in_sym = in_sym.replace('.', '_')
    if in_market in ('nyse', 'nasdaq'):
        url_str = f'https://dividendhistory.org/payout/{in_sym}/'
    else:
        url_str = f'https://dividendhistory.org/payout/{in_market}/{in_sym}/'
    
    try:
        dfs = pd.read_html(url_str)
    except:
        print(f"Could not get {in_market} Div History for {in_sym}")
        return pd.DataFrame()  
            
    # small decision block to deal with optional anoucements header on some pages
    if len(dfs)==3:
        df = dfs[0]
    elif len(dfs)==4:
        df = dfs[1]
    else:
        print('something else going on here')
            
    # drop the last column (i can calculate div increase percentages myself) 
    # clean up dataframe before returning
    
    df['Cash Amount'] = df['Cash Amount'].str.replace('$', '')
    df['Cash Amount'] = df['Cash Amount'].str.replace('\*\*', '')
    df = df.iloc[:, :-1]
    df['Exchange'] = in_market
    df['Symbol'] = in_sym.replace('_', '.')
            
    # fill any empty Payout Date fields with todays date
    # this is a work around for an annoying gap in dataset
    curr_date = {"Payout Date": date.today().strftime("%Y-%m-%d")}
    df = df.fillna(value=curr_date)
            
    df['ex-div date epoch'] = df.apply (lambda x: int(((datetime.datetime.strptime(x['Ex-Dividend Date'], "%Y-%m-%d")).timestamp())*1000), axis=1)
    df['payout date epoch'] = df.apply (lambda x: int(((datetime.datetime.strptime(x['Payout Date'], "%Y-%m-%d")).timestamp())*1000), axis=1)
            
    return df

# simple function to check if a symbol belongs to an exhange 
# based on dividendhistory

def is_in_exchange_DH(in_sym, in_market):
    sym_list = get_tickers_divhistory(in_market)
    return (in_sym in sym_list)

# get and parse weekly stock report from dividendhistory.org
# note:  previous reports are not publicly linked on site but are 
# accessible with URL tweak.
# returns DF with results and adds epoch timstamps

def get_DH_weekly_report(in_market, in_date:date):
     
    
    # check if date is a friday as reports are only published on Fridays
    if su.is_friday(in_date)==su.FAILURE:
        print("DH reports are only published on Fridays - check your date")
        return pd.DataFrame()
    # validate market 
    if in_market in ('nyse', 'nasdaq'):
        market = 'USA'
    elif in_market == 'tsx':
        market = 'CAN'
    else:
        print(f'Market {in_market} not valid')
        return pd.DataFrame()
    
    #data_file_path = "{1}weekly_divhistory_reports/{0}/".format(market, in_file_path)
    web_path = 'https://dividendhistory.org/reports/{3}/{2}-{1}-{0}-report.htm'.format(in_date.strftime("%d"), in_date.strftime("%m"), in_date.year, market)
    #data_file_path = data_file_path + "div_history_report-{3}-{2}-{1}-{0}.csv".format(in_date.strftime("%d"), in_date.strftime("%m"), in_date.year, market)
    try:
        dfs = pd.read_html(web_path, keep_default_na=False)
        #write_file = True
        #i+=1
        #printProgressBar(i + 1, len(fridays), prefix = '{0} Weekly Report Progress:'.format(market), suffix = 'Complete', length = 50)
    except HTTPError as err:
        print(f"Path not found: {err.url}: Code: {err.code}")
        return pd.DataFrame()
        #write_file = False
    
    # take first DataFrame in list 
    df = dfs[0]
    # cut off extra null columns
    df = df.iloc[:, :16]
    
    # clean up - fix column names
    colnames = []
    for col in df.columns:
        colnames.append(col[1])
    df.columns = colnames
            # remove sector category rows from data
            # this function assumes that all cells are populated with same string
            # when its a header row
    for row_num, row in df.iterrows():
        if row['Price'] == row['Name']:
            df = df.drop(row_num)
            
    date_str  = "{0}-{1}-{2}".format(in_date.year, in_date.strftime("%m"), in_date.strftime("%d"))
    df['report_date_epoch'] = int(((datetime.datetime.strptime(date_str, "%Y-%m-%d")).timestamp())*1000)
    # strip % from yld and PayRto
    df['Yld'] = df['Yld'].map(lambda x: x.lstrip('').rstrip('%'))
    df['PayRto'] = df['PayRto'].map(lambda x: x.lstrip('').rstrip('%'))
            
    # split div frequency from ex-div date
    # had to run in a try statement because of at least one report 
    # that had no dates, just frequency for ex-div date .. if this happens,
    # whole div-freq column is set to -
    try:
        df['div_freq'] = (df['Ex-Div'].str.split(pat=r'\d\d\d\d-\d\d-\d\d', expand=True))[1]
        df['Ex-Div'] = df['Ex-Div'].map(lambda x: x.lstrip('').rstrip('AQSMU'))
    except:
        df['div_freq'] = "-"
        pass
    # need to reinsert nans for whitespace cells as nans are removed on import
    # once nans are back in, fillnan with - 
    # all of this is because of one ticker symbol (NA) which is interpreted as a NaN on import
    # unless keep_default_na=false
    df = df.replace(r'^\s*$', np.nan, regex=True)
    df = df.fillna(value='-')
    df['market'] = in_market            
    try:
        df['ex_div_epoch'] = df.apply (lambda x: "-" if x['Ex-Div'] == "-" else int(((datetime.datetime.strptime(x['Ex-Div'], "%Y-%m-%d")).timestamp())*1000), axis=1)
    except:
        df['ex_div_epoch'] = "-"
        
    return df




# --------------------- REMOTE EXTRACTIONS Yahoo ----------------------------


# get and parse price history from yahoo_finance for given ticker 
# and given date range
#   Either in_period = max (full history) or last_day 
#   OR
#   in_period = spec AND requires at least in_start str 'YYYY-MM-DD'
#   no in_end specified will default to today
# returns DataFrame

def get_ticker_price_history_yahoo(in_sym: str, in_market:str, in_period:str, *xargs, **kwargs):
    
    
    if in_market not in su.MARKETS: 
        print('market must be one of TSX, NYSE, or NASDAQ')
        return pd.DataFrame()
    
    if not is_in_exchange_DH(in_sym, in_market):
        print(f'ticker not in exchange {in_sym} is not in {in_market}')
        return pd.DataFrame()
    
    
    # convert standard ticker to yahoo ticker notation
    # replace . with _ 
    # append .(excchange digraph) TSX the only one supported right now
    
    if in_period == 'spec':
        start = kwargs.get('in_start')
        end = kwargs.get('in_end')
        if start!=None:
            if end==None:
                end = date.today() # use yesterday as enddate by default. enddate in yfinance in non-inclusive
        else:
            print('You need to provide a start date with spec')
            return pd.DataFrame()
    
    
    # PREP
    in_sym = in_sym.replace('.', '-')
    if in_market == 'tsx':
        in_sym = in_sym + '.TO'
    curr_tick = yf.Ticker(in_sym)
    
    # auto_adjust set to false to get prices adjusted for splits only (not dividends)
    if in_period == 'max' or in_period =='last_day':    
        df = curr_tick.history(period=in_period, auto_adjust=False)
    else:
        df = curr_tick.history(start=start, end=end, auto_adjust=False)
    if df.empty is False:
        df['symbol'] = in_sym.replace('.TO', '')
        df['market'] = in_market
        df = df.reset_index()
        df['date_epoch'] = df.apply (lambda x: int(x['Date'].timestamp())*1000, axis=1)
        
    else:
        pass
    
    return df


# --------------------------- LOCAL EXTRACTIONS ----------------------------------

# grab divdidend history for ticker from local csv
# original source dividendhistory.org
# returns DataFrame
# EXTRACT
def get_DH_div_history_local(in_data_path:str, in_ticker:str, in_market:str):
    
    if in_market not in su.MARKETS:
        print("Market must be one of tsx, nyse. nasdaq")
        return pd.DataFrame()
    
    try:
        data_file_path = in_data_path
        #temp_tick = in_ticker.replace('.', '_')
        #print(in_ticker)
        dfs = pd.read_csv(f'{data_file_path}{in_market}/DH_div_history_{in_ticker}.csv', keep_default_na=False)
        #div_path = data_file_path + "yield_history/"
        #make_dir(div_path)
    except:
        print(f"Could not find {data_file_path}{in_market}/DH_div_history_{in_ticker}.csv")
        return pd.DataFrame()
    return dfs

# grab weekly DH report from local data store csv
# returns full data frame of report on given day
# in_data_path full root directory for DH reports 
# original source dividendhistory.org
# EXTRACT
def get_DH_weekly_report_local(in_data_path:str, in_market:str, in_date:date):
    
    if in_market not in su.MARKETS:
        print("Market must be one of tsx, nyse. nasdaq")
        return pd.DataFrame()
    if not su.is_friday(in_date):
        print("Date must be a Friday in the past")
        print(in_date)
        return pd.DataFrame()
    
    try:
        if in_market == 'tsx':
            dfs = pd.read_csv(f'{in_data_path}CAN/div_history_report-CAN-{in_date.year}-{in_date.month}-{in_date.day}.csv', keep_default_na=False)
        else:
            dfs = pd.read_csv(f'{in_data_path}USA/div_history_report-USA-{in_date.year}-{in_date.month}-{in_date.day}.csv', keep_default_na=False)
        #dfs.drop(columns=["Name", "Price", "Yld", "Ex-Div", "PayRto", "PE", "PB", "Beta", "Mkt Cap", "WK%", "MO%", "2MO%", "3MO%", "6MO%", "1YR%", "report_date_epoch", "ex_div_epoch"], inplace=True)
    except:
        print(f'Could not find weekly report for {in_market}')
        return pd.DataFrame()
    return dfs

# grab price history for ticker
# in_data_path is full path to directory containing price recrords from yahoo
# returns DataFrame    
# EXTRACT
def get_ticker_price_history_yahoo_local(in_data_path:str, in_market:str, in_ticker:str):
    
    if in_market not in su.MARKETS:
        print("Market must be one of tsx, nyse. nasdaq")
        return pd.DataFrame()
    
    try:
        #if in_market == 'tsx':
        ##    in_ticker_can = in_ticker.replace('.', '-')
          #  in_ticker_can = in_ticker_can + '.TO'
        dfs = pd.read_csv(f'{in_data_path}yahoo_price_history_{in_ticker}_{in_market}.csv', keep_default_na=False)
       # else:
            #in_ticker_us = in_ticker.replace('.', '-')
        #    dfs2 = pd.read_csv(f'{data_file_path}price_history/yahoo_price_history_{in_ticker}.csv')
        
        #print(dfs2)
    except:
        print(f"{in_data_path}yahoo_price_history_{in_ticker}_{in_market}.csv - Failed")
        return pd.DataFrame()
    #print(dfs2)
    return dfs

# get list of tickers sourced from dividendhistory.org from local csv
# 
# returns list of tickers symbols only populated from local copy to divhistory ticker list
# will extract a column named Symbol from provided dataframe and return as a list
# FUTURE : could generalize as extact named column as list

def get_tickers_divhistory_local(in_path, in_file_name):

    try:
        dfs = pd.read_csv(f'{in_path}{in_file_name}', keep_default_na=False)
        #print(dfs)
    except:
        print(f"Could not find file {in_path}{in_file_name}")
        return su.FAILURE
    try:
        sym_list = dfs['Symbol'].to_list()
    except KeyError:
        print("DF does not contain key Symbol")
        return su.FAILURE
    return (sym_list)