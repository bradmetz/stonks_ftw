#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    stonks_flows - contains a set of predefined flows using the stonks
    ETL libraries as examples and to define automated analytic flows
    

"""
import stonks_utils as su
import stonks_extract as se
import stonks_output as so
import stonks_transform as st
import pandas as pd
from datetime import date
from dateutil.relativedelta import relativedelta

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
        if so.df_to_csv(df, data_file_path, f"DH_tickers_{exc}.csv", True)==su.FAILURE:
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


# update each price history document for each ticker based on last 
# date recorded up to yesteday 
# this function meant to be used to update the existing dataset built
# running get_ticker_price_history previously 

# lazy solution is to just run full history collect and 
# overwrite full csv files each night

def update_ticker_price_records(in_tickers: list, in_file_path:str, in_market:str):
    
    # full path to be provided going forward
    #data_file_path = in_file_path
    #data_file_path = data_file_path + 'price_history/' 
    
    # get last record date from file
    i=0
    su.printProgressBar(0, len(in_tickers), prefix = f'{in_market} Price History Progress:', suffix = 'Complete', length = 50)

    
    for curr_sym in in_tickers:
        i += 1
        df = pd.DataFrame()
        su.printProgressBar(i, len(in_tickers), prefix = f'{in_market} Price History Progress:', suffix = 'Complete', length = 50)
        
        try:
            dfs = pd.read_csv(f'{in_file_path}yahoo_price_history_{curr_sym}_{in_market}.csv', keep_default_na=False)
            dfs['Date'] = pd.to_datetime(dfs['Date'])
            last_date = dfs['Date'].max() + relativedelta(days=1)
        except:
            print(f"Could not open {in_file_path}_{curr_sym}_{in_market}.csv")
            pass
        
        if last_date < date.today():
            df = se.get_ticker_price_history_yahoo(curr_sym, in_market, 'spec', in_start=last_date)
    
        if df.empty is False:
            so.append_df_to_csv(df, in_file_path, f'yahoo_price_history_{curr_sym}_{in_market}.csv')
        else:
            pass
    return 0

# extract:  yields, DH, price history from local
# transform: create daily yields based on daily price data set 
# output: write to "yields" directory in datasets under project
# output: calculate and write daily yields using last declared div 

# for each file in market dir 

# TO REFACTOR - add to transform with DF input and output
# prereq - DH weekly report, yahoo_daily_prices


def daily_yield_calc_history(in_market: str, in_data_path: str, in_ticker):
    
    
    
    # read in dividend history,  read in price history, calculate and add daily yield
    # data structure : date, date_epoch, price, dividend, yield
    # PREP
    if in_market not in su.MARKETS: #!= 'tsx' and in_market != 'nyse' and in_market != 'nasdaq':
        print('Market must be one of tsx, nyse, nasdaq')
        return -1
    
    # grab divdidend history for ticker
    # EXTRACT
    
    df_divs = se.get_DH_div_history_local(in_data_path, in_ticker, in_market)
    if df_divs == su.FAILURE:
        print(f"{in_data_path}{in_market}{in_ticker} Failed")
        return su.FAILURE
    
   # try:
   #     data_file_path = in_data_path
   #     temp_tick = in_ticker.replace('.', '_')
   #     #print(in_ticker)
   #     dfs = pd.read_csv(f'{data_file_path}{in_market}/DH_div_history_{temp_tick}.csv', keep_default_na=False)
   #     div_path = data_file_path + "yield_history/"
   #     make_dir(div_path)
   # except:
   #     print(f"Could not find {data_file_path}{in_market}/DH_div_history_{temp_tick}.csv")
   #     return -1
    
    #print(dfs)
    # grab weekly DH report and isolate Div Freq
    # EXTRACT
    #try:
    #    if in_market == 'tsx':
    #        dfs3 = pd.read_csv(f'./datasets/weekly_divhistory_reports/CAN/div_history_report-CAN-2020-08-14.csv', keep_default_na=False)
    #    else:
    #        dfs3 = pd.read_csv(f'./datasets/weekly_divhistory_reports/USA/div_history_report-USA-2020-08-14.csv', keep_default_na=False)
        
    #except:
    #    print(f'Could not find weekly report for {in_market}')
    #    return -1
    in_date = su.get_last_friday()
    
    df_div_freqs = se.get_DH_weekly_report_local(in_data_path+'weekly_divhistory_reports/', in_market, in_date)
    if df_div_freqs == su.FAILURE:
        print(f"{in_data_path}weekly_divhistory_report/ {in_date} Failed")
        return su.FAILURE
    # only want div freq with symbols

    # grab price history for ticker
    # EXTRACT
    #try:
     #   if in_market == 'tsx':
     ##       in_ticker_can = in_ticker.replace('.', '-')
      #      in_ticker_can = in_ticker_can + '.TO'
      #      dfs2 = pd.read_csv(f'{data_file_path}price_history/yahoo_price_history_{in_ticker_can}.csv')
       # else:
        #    in_ticker_us = in_ticker.replace('.', '-')
         #   dfs2 = pd.read_csv(f'{data_file_path}price_history/yahoo_price_history_{in_ticker}.csv')
        
        #print(dfs2)
    #except:
     #   print(f"{data_file_path}price_history/yahoo_price_history_{in_ticker}.csv")
      #  return -1
    #print(dfs2)
    df_prices = se.get_ticker_price_history_yahoo_local(in_data_path+'price_history/', in_market, in_ticker)
    if df_prices == su.FAILURE:
        print(f"{in_data_path}price_history/ {in_market} {in_ticker} - Failure")
        return su.FAILURE
   
    
    # join datasets on date and fill dividends down 
    # TRANSFORM

    result = st.generate_yield_history(df_divs, df_div_freqs, df_prices, in_ticker)
    if(result == su.FAILURE):
        print(f"df_divs {df_divs} : df_div_freqs {df_div_freqs} : df_prices {df_prices} : in_ticker {in_ticker}")
        return su.FAILURE
    

#    df_div_freqs.drop(columns=["Name", "Price", "Yld", "Ex-Div", "PayRto", "PE", "PB", "Beta", "Mkt Cap", "WK%", "MO%", "2MO%", "3MO%", "6MO%", "1YR%", "report_date_epoch", "ex_div_epoch"], inplace=True)
    
 #   df_divs.rename(columns={'Ex-Dividend Date':'Date'}, inplace=True)
 #   result = pd.merge(df_divs, df_prices, on=['Date'], how='outer')
 #   result.sort_values(by='Date', inplace=True)
 #   result.fillna(method='ffill', inplace=True)
 #   result.drop(columns=['Open', 'High', 'Low', 'Dividends', 'symbol', 'market', 'date_epoch', 'Stock Splits'], inplace=True)
    
 #   try:
        # frequency factor
 #       freq = df_div_freqs.loc[df_div_freqs['Symbol'] == in_ticker]
        #print(freq)
  #      if freq.iloc[0]['div_freq'] == 'Q':
  #          yield_factor = 4
  #      elif freq.iloc[0]['div_freq'] == 'S':
  #          yield_factor = 2
  #      elif freq.iloc[0]['div_freq'] == 'M':
  #          yield_factor = 12
  #      elif freq.iloc[0]['div_freq'] == 'A':
  #          yield_factor = 1
   #     else:
            # ignoring U and - for now
    #        yield_factor = 0
    #except:
    #    print("Error getting freq")
    #    return -1
    
    
    # yield calculation
   # result['Daily Yield'] = yield_factor*result['Cash Amount']/result['Close']
    # remove historic price records with no div
   # result = result[result['Daily Yield'].notna()]
    
    #return result
    # OUTPUT
    
    # write out yield history by exchange and ticker
    su.make_dir(f"{in_data_path}yield_history/")
    so.df_to_csv(result, f"{in_data_path}yield_history/", f"yield_history_{in_market}_{in_ticker}.csv", False)
    #print(f"Path to write out {data_file_path}yield_history/yield_history_{in_market}_{in_ticker}.csv")
    #result.to_csv(f"{data_file_path}yield_history/yield_history_{in_market}_{in_ticker}.csv", index=0)
    
    return su.SUCCESS