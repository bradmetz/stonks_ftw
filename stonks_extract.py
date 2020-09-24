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

import stonks_utils as su

# get summary of tickers from dividendhistory.org
# in_market is one of tsx, nyse, nasdaq
# adds exchange and epoch time stamp for next ex-div
# returns a dataframe with the following structure 
# Symbol, Company, Yield Percentage, Next Ex-div Date, Exchange, ex-div epoch


def get_ticker_summary_divhistory(in_market: str):
    
    if not (in_market in su.MARKETS):
        print('in_market must be one of tsx, nyse, nasdaq')
        return su.FAILURE
    
    try:
        dfs = pd.read_html(f'https://dividendhistory.org/{in_market}', keep_default_na=False, header=0, index_col=0)
    except HTTPError as err:
        print(f"Could not get TSX ticks: HTTP Code: {err.code}  Path Tried: {err.url}")
        return su.FAILURE
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
        print(f"Could not get TSX ticks: HTTP Code: {err.code}  Path Tried: {err.url}")
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
        return su.FAILURE
    
    in_sym = in_sym.replace('.', '_')
    if in_market in ('nyse', 'nasdaq'):
        url_str = f'https://dividendhistory.org/payout/{in_sym}/'
    else:
        url_str = f'https://dividendhistory.org/payout/{in_market}/{in_sym}/'
    
    try:
        dfs = pd.read_html(url_str)
    except:
        print(f"Could not get {in_market} Div History for {in_sym}")
        return su.FAILURE    
            
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


# get list of tickers sourced from dividendhistory.org from local csv
# 
# returns list of tickers symbols only populated from local copy to divhistory ticker list
# will extract a column named Symbol from provided dataframe and return as a list
# FUTURE : could generalize as extact named column as list

def get_tickers_divhistory_local(in_path, in_file_name):

    try:
        dfs = pd.read_csv(f'{in_path}{in_file_name}', keep_default_na=False)
    except:
        print(f"Could not find file {in_path}{in_file_name}")
        return su.FAILURE
    try:
        sym_list = dfs['Symbol'].to_list()
    except KeyError:
        print("DF does not contain key Symbol")
        return su.FAILURE
    return (sym_list)


