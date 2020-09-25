#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    stonks_flows - contains a set of predefined flows using the stonks
    ETL libraries as examples and to define automated analytic flows
    

"""
import stonks_utils as su
import stonks_extract as se
import stonks_output as so
import pandas as pd

# get all dividend histories from dividendhistory.org and save to provided file path
# in_file_path is the root dataset path with trailing '/' 
# other directories will be created in here so should be writable
def get_div_histories_DH(in_file_path):
    
    data_file_path = in_file_path
    
    for exc in su.MARKETS:
        ticks = se.get_tickers_divhistory(exc)
        div_path = data_file_path + f"{exc}/"
        i=0
        su.printProgressBar(0, len(ticks), prefix = f'{exc} Div History Progress:', suffix = 'Complete', length = 50)
        for sym in ticks: 
            i+=1
            su.printProgressBar(i, len(ticks), prefix = f'{exc} Div History Progress:', suffix = 'Complete', length = 50)
            dfs = se.get_div_history_DH(sym, exc)
            so.df_to_csv(dfs, div_path, f"DH_div_history_{sym}.csv", False)
    return su.SUCCESS
    
# flow used to get tickers and other info from divhistory
# kept as is for backward compatibility

def getTickers(in_file_path):
    data_file_path = in_file_path
    
    for exc in su.MARKETS:
        df = se.get_ticker_summary_divhistory(exc)
        if so.df_to_csv(df, data_file_path, f"DH_tickers_{exc}.csv", False)==su.FAILURE:
            print(f"Error writing DH_tickers_{exc}.csv")
            
    return su.SUCCESS

# flow to download all dividendhistory weekly reports and save to separate csvs
# for later use from a given market
# using datetime.date as default date container

# in_file_path is the full path to where the reports are stored

def dl_and_write_DH_reports(in_file_path, in_market, *args, **kwargs):
    
    in_year = kwargs.get('year')
    update = kwargs.get('update')
    fridays = {}
    
    # PREP
    # given the year, gets reports for all Fridays from that year forward
    # not reports prior to 2019
    
    if in_year != None:    
        if in_year < 2019:
            print("There are no reports prior to 2019.  Enter year 2019 or greater")
            return su.FAILURE
        elif in_year>2018:
            print(in_year)
            fridays = su.all_fridays_from(in_year)
            print('running from year')
        else:
            print("No fridays returned")
            return su.FAILURE
    
    
    if update==True:
        fridays = su.fridays_since_last_DH_report(in_file_path, in_market)
        if len(fridays)<1:
            print("no new fridays returned on update")
            return su.FAILURE
    
    if in_market in ('nyse', 'nasdaq'):
        in_country = 'USA'
        in_file_path += 'USA/'
    elif in_market == 'tsx':
        in_country = 'CAN'
        in_file_path += 'CAN/'
    else:
        print("Market {in_market} is invalid")
        return se.FAILURE
    
    # download reports for all fridays in fridays stonks_extract
    # write out using stonks_output
    i=0
    su.printProgressBar(0, len(fridays), prefix = '{0} Weekly Report Progress:'.format(in_market), suffix = 'Complete', length = 50)
    for fri in fridays:
        
        i +=1
        su.printProgressBar(i, len(fridays), prefix = '{0} Weekly Report Progress:'.format(in_market), suffix = 'Complete', length = 50)
        # EXTRACT
        df = se.get_DH_weekly_report(in_market, fri)
        
        # OUTPUT
        if type(df) != pd.DataFrame:
            print(f"no report for {in_market} on {fri.year}-{fri.month}-{fri.day}")
        elif so.df_to_csv(df, in_file_path, f"div_history_report-{in_country}-{fri.year}-{fri.month}-{fri.day}.csv", False)==su.FAILURE:
            print(f"Error writing div_history_report-{in_country}-{fri.year}-{fri.month}-{fri.day}.csv")
    return su.SUCCESS


# flow to download all price histories from yahoo and save as csv locally
# default to all full history
# in_file_path is full path to price history directory and histories are 
# saved as one file per ticker

def get_ticker_price_history(in_tickers: list, in_file_path:str, in_market:str):
    
    # setup based on input parameters
    #data_file_path = data_file_path + 'price_history/'
    su.make_dir(in_file_path)
    i=0
    su.printProgressBar(0, len(in_tickers), prefix = f'{in_market} Price History Progress:', suffix = 'Complete', length = 50)
    for curr_sym in in_tickers:
        i += 1
        su.printProgressBar(i, len(in_tickers), prefix = f'{in_market} Price History Progress:', suffix = 'Complete', length = 50)
        # EXTRACT
        df = se.get_ticker_price_history_yahoo(curr_sym, in_market, 'max')
        
        # OUTPUT
        if type(df) != pd.DataFrame:
            print(f"Error collecting price history for {curr_sym} on {in_market}")
        elif so.df_to_csv(df, in_file_path, f"yahoo_price_history_{curr_sym}_{in_market}.csv", False) == su.FAILURE:
            print(f"Error writing file for {curr_sym} in market {in_market}")
            
    return su.SUCCESS