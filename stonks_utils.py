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


# generalize function to take a list of tickers instead of a pandas dataframe
# returns 0 on success -1 otherwise
# default time period is "max" 
# write all price histories to in_file_path/price_histories
# may need to rethink how i code the daily updater code

def get_ticker_price_history(in_tickers: list, in_period, in_file_path, in_market):
    
    
    data_file_path = in_file_path
    data_file_path = data_file_path + 'price_history/'
    make_dir(data_file_path)
    if in_period == 'max':
        print("got max")
    # needed for daily automated updates
    elif in_period == 'last_day':
        print("got last_day")
    else:
        print('Only \'max\' and \'last_day\' supported as this time')
        return -1
    
    if in_market != 'TSX' and in_market != 'NYSE' and in_market != 'NASDAQ':
        print('market must be one of TSX, NYSE, or NASDAQ')
        return -1
    
    for curr_sym in in_tickers:
        curr_sym = curr_sym.replace('.', '-')
        if in_market == 'TSX':
            curr_sym = curr_sym + '.TO'
        curr_tick = yf.Ticker(curr_sym)
        ret_df = curr_tick.history(period=in_period)
        ret_df['symbol'] = curr_sym
        ret_df['market'] = in_market
        ret_df.to_csv(f'{data_file_path}yahoo_price_history_{curr_sym}.csv')
        
    return 0
        


# in_file_path is the root dataset path with trailing '/' 
# other directories will be created in here so should be writable
def get_div_histories_DH(in_file_path):
    
    data_file_path = in_file_path
    # TSX dividend history download 
    dfs = pd.read_csv(f'{data_file_path}DH_tickers_tsx.csv', keep_default_na=False)
    ticks = dfs.iloc[:, 0:1]
    div_path = data_file_path + "tsx/"
    make_dir(div_path)
    i=0
    printProgressBar(0, len(ticks), prefix = 'TSX Div History Progress:', suffix = 'Complete', length = 50)
    # loop throuigh all tickers and create new csv for each div stock
    for (sym_index, sym_val) in ticks.iteritems():
        #needed to deal with '.'s in ticker symbols (eg ATB.B)
        for sym in sym_val.values:
            i+=1
            printProgressBar(i, len(ticks), prefix = 'TSX Div History Progress:', suffix = 'Complete', length = 50)
            sym = sym.replace('.', '_')
            try:
                dfs = pd.read_html(f'https://dividendhistory.org/payout/tsx/{sym}/')
            except:
                print(f"Could not get TSX Div History for {sym}")
            # small decision block to deal with optional anoucements header on some pages
            if len(dfs)==3:
                df = dfs[0]
            elif len(dfs)==4:
                df = dfs[1]
            else:
                print('something else going on here')
            # drop the last column (i can calculate div increase percentages myself) 
            df['Cash Amount'] = df['Cash Amount'].str.replace('$', '')
            df['Cash Amount'] = df['Cash Amount'].str.replace('\*\*', '')
            df = df.iloc[:, :-1]
            df['Exchange'] = 'TSX'
            df['Symbol'] = sym
            # fill any empty Payout Date fields with todays date
            # this is a work around for an annoying gap in dataset
            curr_date = {"Payout Date": date.today().strftime("%Y-%m-%d")}
            df = df.fillna(value=curr_date)
            
            df['ex-div date epoch'] = df.apply (lambda x: int(((datetime.datetime.strptime(x['Ex-Dividend Date'], "%Y-%m-%d")).timestamp())*1000), axis=1)
            df['payout date epoch'] = df.apply (lambda x: int(((datetime.datetime.strptime(x['Payout Date'], "%Y-%m-%d")).timestamp())*1000), axis=1)
            
            df.to_csv(f'{div_path}DH_div_history_{sym}.csv', index=False)
    
    # NYSE dividend history download
    dfs = pd.read_csv(f'{data_file_path}DH_tickers_nyse.csv', keep_default_na=False)
    ticks = dfs.iloc[:, 0:1]
    div_path = data_file_path + "nyse/"
    make_dir(div_path)
    # loop throuigh all tickers and create new csv for each div stock
    i=0
    printProgressBar(0, len(ticks), prefix = 'NYSE Div History Progress:', suffix = 'Complete', length = 50)
    for (sym_index, sym_val) in ticks.iteritems():
        #needed to deal with '.'s in ticker symbols (eg ATB.B)
        for sym in sym_val.values:
            i+=1
            printProgressBar(i, len(ticks), prefix = 'NYSE Div History Progress:', suffix = 'Complete', length = 50)
            sym = sym.replace('.', '_')
            try:
                dfs = pd.read_html(f'https://dividendhistory.org/payout/{sym}/')
            except:
                print(f"Could not get NYSE Div History for {sym}")
            # small decision block to deal with optional anoucements header on some pages
            if len(dfs)==3:
                df = dfs[0]
            elif len(dfs)==4:
                df = dfs[1]
            else:
                print('something else going on here')
            # drop the last column (i can calculate div increase percentages myself) 
            df['Cash Amount'] = df['Cash Amount'].str.replace('$', '')
            df['Cash Amount'] = df['Cash Amount'].str.replace('\*\*', '')
            df = df.iloc[:, :-1]
            df['Exchange'] = 'NYSE'
            df['Symbol'] = sym
            
             # fill any empty Payout Date fields with todays date
            # this is a work around for an annoying gap in dataset
            curr_date = {"Payout Date": date.today().strftime("%Y-%m-%d")}
            df = df.fillna(value=curr_date)
            
            # need to check for post processing dataframes that are empty.
            # this occurs when a company has just started paying dividends since 
            # future dividend records are currenlty removed ... may look at adding them back in
        
            df['ex-div date epoch'] = df.apply (lambda x: int(((datetime.datetime.strptime(x['Ex-Dividend Date'], "%Y-%m-%d")).timestamp())*1000), axis=1)
            df['payout date epoch'] = df.apply (lambda x: int(((datetime.datetime.strptime(x['Payout Date'], "%Y-%m-%d")).timestamp())*1000), axis=1)
            df.to_csv(f'{div_path}DH_div_history_{sym}.csv', index=False)
    
    # NASDAQ dividend history download
    dfs = pd.read_csv(f'{data_file_path}DH_tickers_nasdaq.csv', keep_default_na=False)
    ticks = dfs.iloc[:, 0:1]
    div_path = data_file_path + "nasdaq/"
    make_dir(div_path)
    # loop throuigh all tickers and create new csv for each div stock
    i=0
    printProgressBar(0, len(ticks), prefix = 'NASDAQ Div History Progress:', suffix = 'Complete', length = 50)
    for (sym_index, sym_val) in ticks.iteritems():
        #needed to deal with '.'s in ticker symbols (eg ATB.B)
        for sym in sym_val.values:
            i+=1
            printProgressBar(i, len(ticks), prefix = 'NASDAQ Div History Progress:', suffix = 'Complete', length = 50)
            sym = sym.replace('.', '_')
            try:
                dfs = pd.read_html(f'https://dividendhistory.org/payout/{sym}/')
            except:
                print(f"Could not get NASDAQ Div History for {sym}")
            # small decision block to deal with optional anoucements header on some pages
            if len(dfs)==3:
                df = dfs[0]
            elif len(dfs)==4:
                df = dfs[1]
            else:
                print('something else going on here')
            # drop the last column (i can calculate div increase percentages myself) 
            df['Cash Amount'] = df['Cash Amount'].str.replace('$', '')
            df['Cash Amount'] = df['Cash Amount'].str.replace('\*\*', '')
            df = df.iloc[:, :-1]
            df['Exchange'] = 'NASDAQ'
            df['Symbol'] = sym
            
            # fill any empty Payout Date fields with todays date
            # this is a work around for an annoying gap in dataset
            curr_date = {"Payout Date": date.today().strftime("%Y-%m-%d")}
            df = df.fillna(value=curr_date)
            
            df['ex-div date epoch'] = df.apply (lambda x: int(((datetime.datetime.strptime(x['Ex-Dividend Date'], "%Y-%m-%d")).timestamp())*1000), axis=1)
            df['payout date epoch'] = df.apply (lambda x: int(((datetime.datetime.strptime(x['Payout Date'], "%Y-%m-%d")).timestamp())*1000), axis=1)
            
            df.to_csv(f'{div_path}DH_div_history_{sym}.csv', index=False)

# ticker lists stores in root data directory
# in_file_path is the root dataset directory with trailing '/'
def getTickers(in_file_path):
    data_file_path = in_file_path
    try:
        dfs = pd.read_html('https://dividendhistory.org/tsx', keep_default_na=False, header=0, index_col=0)
    except:
        print("Could not get TSX ticks")
        sys.exit(1)
    df = dfs[0]
    df['Exchange'] = "TSX"
    df['ex-div epoch'] = df.apply (lambda x: int(((datetime.datetime.strptime(x['Next Ex-div Date'], "%Y-%m-%d")).timestamp())*1000), axis=1)
    df.to_csv(f'{data_file_path}DH_tickers_tsx.csv')
    
    try:
        dfs = pd.read_html('https://dividendhistory.org/nyse', keep_default_na=False, header=0, index_col=0)
    except:
        print("Could not get NYSE ticks")
        sys.exit(1)
    df = dfs[0]
    df['Exchange'] = "NYSE"
    df['ex-div epoch'] = df.apply (lambda x: int(((datetime.datetime.strptime(x['Next Ex-div Date'], "%Y-%m-%d")).timestamp())*1000), axis=1)
    df.to_csv(f'{data_file_path}DH_tickers_nyse.csv')
    
    try:
        dfs = pd.read_html('https://dividendhistory.org/nasdaq', keep_default_na=False, header=0, index_col=0)
    except:
        print("Could not get NASDAQ")
        sys.exit(1)
    df = dfs[0]
    df['Exchange'] = "NASDAQ"
    df['ex-div epoch'] = df.apply (lambda x: int(((datetime.datetime.strptime(x['Next Ex-div Date'], "%Y-%m-%d")).timestamp())*1000), axis=1)
    df.to_csv(f'{data_file_path}DH_tickers_nasdaq.csv')


#return 0 on success and -1 on error
#in_file_path = base data directory ... subfolders will be created in here
def dl_and_write_DH_reports(in_file_path, year: int, market):
    
    if market != "USA" and market!= "CAN":
        print("Market string must be one of USA or CAN")
        return -1
    if year < 2019:
        print("There are no reports prior to 2019.  Enter year 2019 or greater")
        return -1
    
    write_file = True
    data_file_path = "{1}weekly_divhistory_reports/{0}/".format(market, in_file_path)
    make_dir(data_file_path)
    fridays = all_fridays_from(year)
    i = 0
    printProgressBar(0, len(fridays), prefix = '{0} Weekly Report Progress:'.format(market), suffix = 'Complete', length = 50)
    for day in fridays:      
        data_file_path = "{1}weekly_divhistory_reports/{0}/".format(market, in_file_path)
        web_path = 'https://dividendhistory.org/reports/{3}/{2}-{1}-{0}-report.htm'.format(day.strftime("%d"), day.strftime("%m"), day.year, market)
        data_file_path = data_file_path + "div_history_report-{3}-{2}-{1}-{0}.csv".format(day.strftime("%d"), day.strftime("%m"), day.year, market)
        try:
            dfs = pd.read_html(web_path, keep_default_na=False)
            write_file = True
            i+=1
            printProgressBar(i + 1, len(fridays), prefix = '{0} Weekly Report Progress:'.format(market), suffix = 'Complete', length = 50)
        except:
            #print(f"File not found: {web_path}")
            write_file = False
        
        # write_file flag is used to indicate the webresource was found
        # and prevents trying to write a non-existent dataframe
        if write_file: 
            df = dfs[0]
            df = df.iloc[:, :16]
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
            
            date_str  = "{0}-{1}-{2}".format(day.year, day.strftime("%m"), day.strftime("%d"))
            df['report_date_epoch'] = int(((datetime.datetime.strptime(date_str, "%Y-%m-%d")).timestamp())*1000)
            # strip % from yld and PayRto
            df['Yld'] = df['Yld'].map(lambda x: x.lstrip('').rstrip('%'))
            df['PayRto'] = df['PayRto'].map(lambda x: x.lstrip('').rstrip('%'))
            
            # split div frequency from ex-div date
            # had to run in a try statement because of at least one report 
            # that had no dates, just requency for ex-div date .. if this happens,
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
            df['market'] = market            
            try:
                df['ex_div_epoch'] = df.apply (lambda x: "-" if x['Ex-Div'] == "-" else int(((datetime.datetime.strptime(x['Ex-Div'], "%Y-%m-%d")).timestamp())*1000), axis=1)
            except:
                df['ex_div_epoch'] = "-"
                #print("Exception tripped")
                pass
            # write out the fixed up report
            df.to_csv(data_file_path, index=0)
    printProgressBar(len(fridays), len(fridays), prefix = '{0} Weekly Report Progress:'.format(market), suffix= 'Complete', length=50)
    return 0


# returns an array of datetime objects of all fridays from the year given 
# to the last Friday from the current day
def all_fridays_from(in_year: int):
    fridays = []
    current_date = datetime.datetime.now()
    for year in range(in_year, current_date.year+1):
        for month in range (1, 13):
            cal = calendar.monthcalendar(year, month)
            for week in cal:
                if week[calendar.FRIDAY] != 0:
                    x = datetime.datetime(year, month, week[calendar.FRIDAY])
                    if x<current_date:
                        fridays.append(x)
    return fridays


# assumes a date format YYYY-MM-DD 
def str_date_to_epoch(in_date_str):
    date_epoch = datetime.datetime.strptime(in_date_str, "%Y-%m-%d")
    return date_epoch.timestamp()


def make_dir(path):
    if not os.path.exists(path):
        try:
            os.makedirs(path)
            print(f"Directory {path} created")
        except PermissionError:
            print(f"Permission to create directory {path} DENIED ... quitting.")
            sys.exit(1)
    else:
        print(f"Directory {path} already exists ... going to use it for temp ticker store")

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