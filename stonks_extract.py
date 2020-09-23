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