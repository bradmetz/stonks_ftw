#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Daily collector script grabs all data updates for specified  symbols from TSX, NASDAQ, and NYSE 
that pay a dividend based on dividendhistory.org and yfinance.  This script is meant 
to be used as a collector for a single day's worth of data.  Default time will be 
previous day from run unless otherwise specified.

Default updates will be for all data types and sources for the previous day. 

options to consider 
    - date (default: today)
    - market (TSX, NYSE, NASDAQ, default: all)
    - data source (default: all)
        -p --price : grabs closing price from date specified (default: previous day )
        -d --div : grabs dividend history update from date specified (default: previous day)
        -w --weekly : grab weekly DH report from previous week from date specified
        -a --all : grabs all of the above 

"""
import sys, getopt
import pandas as pd
from datetime import date, timedelta 
import stonks_utils

def main():
    
    global data_file_path
    data_file_path = "./datasets/"
    curr_date = date.today()
    yesterday = curr_date - timedelta(days=1)
    last_friday = stonks_utils.get_last_friday()
    parse_args()
    
    # get current date
    # get list of tickers
    # get updated dividend records 
    #   check previous lastest date
    #   check new date
    #   if differnet, write change
    # get price update
    #   check is previous day already has record
    #   if not, grab and write new record from previous day
    # get DH weekly
    #   get last Friday (from date specified)
    #   check if report from last Friday exists
    #   if not : grab and write
    
    # TSX price updates
    
    ticks = stonks_utils.read_tickers_DH_local('./datasets/', 'tsx')
    stonks_utils.update_ticker_price_records(ticks, './datasets/', 'TSX' )
    ticks = stonks_utils.read_tickers_DH_local('./datasets/', 'nyse')
    stonks_utils.update_ticker_price_records(ticks, './datasets/', 'NYSE' )
    ticks = stonks_utils.read_tickers_DH_local('./datasets/', 'nasdaq')
    stonks_utils.update_ticker_price_records(ticks, './datasets/', 'NASDAQ' )

   
    
def parse_args():
    global data_file_path
    try:
        opts, args = getopt.getopt(sys.argv[1:], "t:h", ["help", "temp="])
    except getopt.GetoptError:
        usage()
    for o, a in opts:
        if o in ("-t", "--temp"):
            data_file_path = str(a)
            print("Data file path: {}".format(data_file_path))
        if o in ("-h", "--help"):
            usage()
    stonks_utils.make_dir(data_file_path)
    
def usage():
    print ('-----------------------------------------------------------')
    print ('Collector script for stonksftw stock analysis project')
    print ('Use this to automate routine collection and update of data sources')
    print ('Usage: initialize.py [|-t] ')
    print ('-t --temp : specify temp directory to store tickers prior to elastic load (default is <projectdir>/datasets')
    print ('')    
    print ('-----------------------------------------------------------')
    sys.exit(' ')


if __name__ == "__main__":
    main()

