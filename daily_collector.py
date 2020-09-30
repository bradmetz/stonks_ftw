#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Daily collector script grabs all data updates for specified  symbols from TSX, NASDAQ, and NYSE 
that pay a dividend based on dividendhistory.org and yfinance.  This script is meant 
to be used as a collector for a single day's worth of data.  Default time will be 
previous day from run unless otherwise specified.

Assumes the dataset was alrady initialized with initialize.py

Default updates will be for all data types and sources for the previous day. 

options to consider 
    - date (default: today)
    - market (TSX, NYSE, NASDAQ, default: all)
    - data source (default: all)
        -p --price : grabs closing price from last collection date updated flat files
        -d --div : grabs dividend history update from date specified (currently completely replaces existing records)
        -w --weekly : grab weekly DH reports since last collection date 

"""
import sys, getopt
#import pandas as pd
#from datetime import date, timedelta 
import stonks_utils as su
import stonks_extract as se
import stonks_flows as sf

LOCAL_DATASET_PATH = "./datasets/"

def main():
    
    
    global price
    global weekly
    global divs
    price = False
    weekly = False
    divs = False
    
    parse_args()
    
    if price is True:
        for exc in su.MARKETS:
            ticks = se.get_tickers_divhistory_local(LOCAL_DATASET_PATH, f'DH_tickers_{exc}.csv')
            if ticks == su.FAILURE:
                print(f"Error getting tickers {LOCAL_DATASET_PATH}DH_tickers_{exc}.csv")
                return su.FAILURE
            
            sf.update_ticker_price_records(ticks, LOCAL_DATASET_PATH + 'price_history/', exc )
    # weekly report updates based on last report
    if weekly is True:
        sf.dl_and_write_DH_reports(LOCAL_DATASET_PATH+'weekly_divhistory_reports/', "USA", update=True)
        sf.dl_and_write_DH_reports(LOCAL_DATASET_PATH+'weekly_divhistory_reports/', "CAN", update=True)
   # update historic dividend records
   # still lazy method of redownload the entire dataset
    if divs is True:
        sf.get_div_histories_DH(LOCAL_DATASET_PATH)    
    
    if yields is True:
        for exc in su.MARKETS:
            errors = sf.generate_and_save_all_yield_histories(exc, LOCAL_DATASET_PATH)
            print(f"Errors generating yield history {exc} : {errors}")

    return 0
    
def parse_args():
    #global data_file_path
    global price
    global divs
    global weekly
    global yields
    try:
        opts, args = getopt.getopt(sys.argv[1:], "t:hpwdy", ["help", "temp=", "price", "divs", "weekly", "yield"])
    except getopt.GetoptError:
        usage()
    for o, a in opts:
        #if o in ("-t", "--temp"):
         #   data_file_path = str(a)
          #  print("Data file path: {}".format(data_file_path))
        if o in ("-h", "--help"):
            usage()
        if o in ("-p", "--price"):
            price = True
            print("Getting Price updates")
        if o in ('-w', '--weekly'):
            weekly=True
            print("getting weekly report updates")
        if o in ('-d', '--divs'):
            divs=True
            print("getting dividend updates")
        if o in ('-y', '--yield'):
            yields=True
            print("Calculating yield\ updates")
            
    #su.make_dir(data_file_path)
    
def usage():
    print ('-----------------------------------------------------------')
    print ('Collector script for stonksftw stock analysis project')
    print ('Use this to automate routine collection and update of data sources')
    print ('Usage: initialize.py [|-t] ')
    print ('-t --temp : specify temp directory to store data (default is <projectdir>/datasets')
    print ('-p --price : no argument.  grabs updated prices since last collection date')
    print ('-d --div : no argument.  grabs updated per ticker dividend records since last collection date')
    print ('-w --weekly : no argument.  grabs updated weekly DH reports since last collection date')
    print ('')    
    print ('-----------------------------------------------------------')
    sys.exit(' ')


if __name__ == "__main__":
    main()

