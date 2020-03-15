#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 19:54:22 2020

@author: brad
"""

import pandas as pd
import calendar, datetime, os, sys


def main():
     
    dl_and_write_DH_reports(2019, "USA")
    dl_and_write_DH_reports(2019, "CAN")


# in_file_path is the root dataset path with trailing '/' 
# other directories will be created in here so should be writable
def get_div_histories_DH(in_file_path):
    
    data_file_path = in_file_path
    getTickers()
    
    # TSX dividend history download 
    dfs = pd.read_csv(f'{data_file_path}DH_tickers_tsx.csv', keep_default_na=False)
    ticks = dfs.iloc[:, 0:1]
    div_path = data_file_path + "tsx/"
    make_dir(div_path)
    # loop throuigh all tickers and create new csv for each div stock
    for (sym_index, sym_val) in ticks.iteritems():
        #needed to deal with '.'s in ticker symbols (eg ATB.B)
        for sym in sym_val.values:
            sym = sym.replace('.', '_')
            print(f"https://dividendhistory.org/payout/tsx/{sym}/")
            dfs = pd.read_html(f'https://dividendhistory.org/payout/tsx/{sym}/')
    # small decision block to deal with optional anoucements header on some pages
            if len(dfs)==3:
                df = dfs[0]
            elif len(dfs)==4:
                df = dfs[1]
            else:
                print('something else going on here')
             # dropthe first two rows since they are unconfirmed
            # drop the last column (i can calculate div increase percentages myself) 
            df['Cash Amount'] = df['Cash Amount'].str.replace('$', '')
            df = df.iloc[2:, :-1]
            df['Symbol'] = sym
            df.to_csv(f'{div_path}DH_div_history_{sym}.csv', index=False)
    
    # NYSE dividend history download
    dfs = pd.read_csv(f'{data_file_path}DH_tickers_nyse.csv', keep_default_na=False)
    ticks = dfs.iloc[:, 0:1]
    div_path = data_file_path + "nyse/"
    make_dir(div_path)
    # loop throuigh all tickers and create new csv for each div stock
    for (sym_index, sym_val) in ticks.iteritems():
        #needed to deal with '.'s in ticker symbols (eg ATB.B)
        for sym in sym_val.values:
            sym = sym.replace('.', '_')
            print(f"https://dividendhistory.org/payout/{sym}/")
            dfs = pd.read_html(f'https://dividendhistory.org/payout/{sym}/')

    # small decision block to deal with optional anoucements header on some pages
            if len(dfs)==3:
                df = dfs[0]
            elif len(dfs)==4:
                df = dfs[1]
            else:
                print('something else going on here')
            # dropthe first two rows since they are unconfirmed
            # drop the last column (i can calculate div increase percentages myself) 
            df['Cash Amount'] = df['Cash Amount'].str.replace('$', '')
            df = df.iloc[2:, :-1]
            df['Symbol'] = sym
            df.to_csv(f'{div_path}DH_div_history_{sym}.csv', index=False)
    
    # NASDAQ dividend history download
    dfs = pd.read_csv(f'{data_file_path}DH_tickers_nasdaq.csv', keep_default_na=False)
    ticks = dfs.iloc[:, 0:1]
    div_path = data_file_path + "nasdaq/"
    make_dir(div_path)
    # loop throuigh all tickers and create new csv for each div stock
    for (sym_index, sym_val) in ticks.iteritems():
        
        #needed to deal with '.'s in ticker symbols (eg ATB.B)
        for sym in sym_val.values:
            sym = sym.replace('.', '_')
            print(f"https://dividendhistory.org/payout/{sym}/")
            dfs = pd.read_html(f'https://dividendhistory.org/payout/{sym}/')
    # small decision block to deal with optional anoucements header on some pages
            if len(dfs)==3:
                df = dfs[0]
            elif len(dfs)==4:
                df = dfs[1]
            else:
                print('something else going on here')
            # dropthe first two rows since they are unconfirmed
            # drop the last column (i can calculate div increase percentages myself) 
            df['Cash Amount'] = df['Cash Amount'].str.replace('$', '')
            df = df.iloc[2:, :-1]
            df['Symbol'] = sym
            df.to_csv(f'{div_path}DH_div_history_{sym}.csv', index=False)

# ticker lists stores in root data directory
# in_file_path is the root dataset directory with trailing '/'
def getTickers(in_file_path):
    data_file_path = in_file_path
    dfs = pd.read_html('https://dividendhistory.org/tsx', keep_default_na=False, header=0, index_col=0)
    df = dfs[0]
    df.to_csv(f'{data_file_path}DH_tickers_tsx.csv')
    
    dfs = pd.read_html('https://dividendhistory.org/nyse', keep_default_na=False, header=0, index_col=0)
    df = dfs[0]
    df.to_csv(f'{data_file_path}DH_tickers_nyse.csv')
    
    dfs = pd.read_html('https://dividendhistory.org/nasdaq', keep_default_na=False, header=0, index_col=0)
    df = dfs[0]
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
    printProgressBar(0, len(fridays), prefix = '{0}Progress:'.format(market), suffix = 'Complete', length = 50)
    for day in fridays:      
        data_file_path = "{1}weekly_divhistory_reports/{0}/".format(market, in_file_path)
        web_path = 'https://dividendhistory.org/reports/USA/{2}-{1}-{0}-report.htm'.format(day.strftime("%d"), day.strftime("%m"), day.year)
        data_file_path = data_file_path + "div_history_report-{2}-{1}-{0}.csv".format(day.strftime("%d"), day.strftime("%m"), day.year)
        try:
            dfs = pd.read_html(web_path)
            write_file = True
            i+=1
            printProgressBar(i + 1, len(fridays), prefix = '{0}Progress:'.format(market), suffix = 'Complete', length = 50)
        except:
            #print(f"File not found: {web_path}")
            write_file = False
        
        # write_file flag is used to indicate the webresource was found
        # and prevents trying to write a non-existent dataframe
        if write_file: 
            df = dfs[0]
            df = df.iloc[:, :16]
            #print(df.columns)
            colnames = []
            for col in df.columns:
                colnames.append(col[1])
                #print(col[1])
            df.columns = colnames
            # remove sector category rows from data
            # this function assumes that all cells are populated with same string
            # when its a header row
            for row_num, row in df.iterrows():
                if row['Price'] == row['Name']:
                    df = df.drop(row_num)
                    #3print(f"Removed {row['Price']} number {row_num}")
            
            
            # write out the fixed up report
            df.to_csv(data_file_path, index=0)
    printProgressBar(len(fridays), len(fridays), prefix = '{0}Progress:'.format(market), suffix= 'Complete', lenght=50)
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

if __name__ == "__main__":
    main()

