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
        -p --price : grabs closing price from last collection date updated flat files
        -d --div : grabs dividend history update from date specified (currently completely replaces existing records)
        -w --weekly : grab weekly DH reports since last collection date 

"""
import sys, getopt
#import pandas as pd
#from datetime import date, timedelta 
import stonks_utils

def main():
    
    global data_file_path
    global price
    global weekly
    global divs
    price = False
    weekly = False
    divs = False
    
    data_file_path = "./datasets/"
    #curr_date = date.today()
    #yesterday = curr_date - timedelta(days=1)
    #last_friday = stonks_utils.get_last_friday()
    parse_args()
    
    # get updated dividend records 
    #   check previous lastest date
    #   check new date
    #   if differnet, write change
    # 
    #Update price records will grab all daily closing prices from the last 
    # retrieved price record
    # get DH weekly
    #   run dl_and_write_DH_reports with update=True to grab missing DH weekly reports
    if price is True:
        ticks = stonks_utils.read_tickers_DH_local('./datasets/', 'tsx')
        stonks_utils.update_ticker_price_records(ticks, './datasets/', 'TSX' )
        ticks = stonks_utils.read_tickers_DH_local('./datasets/', 'nyse')
        stonks_utils.update_ticker_price_records(ticks, './datasets/', 'NYSE' )
        ticks = stonks_utils.read_tickers_DH_local('./datasets/', 'nasdaq')
        stonks_utils.update_ticker_price_records(ticks, './datasets/', 'NASDAQ' )
    
    # weekly report updates based on last report
    if weekly is True:
        stonks_utils.dl_and_write_DH_reports(data_file_path, "USA", update=True)
        stonks_utils.dl_and_write_DH_reports(data_file_path, "CAN", update=True)

   # update historic dividend records
    if divs is True:
        stonks_utils.get_div_histories_DH(data_file_path)      
    
    return 0
    
def parse_args():
    global data_file_path
    global price
    global divs
    global weekly
    try:
        opts, args = getopt.getopt(sys.argv[1:], "t:hpwd", ["help", "temp=", "price", "divs", "weekly"])
    except getopt.GetoptError:
        usage()
    for o, a in opts:
        if o in ("-t", "--temp"):
            data_file_path = str(a)
            print("Data file path: {}".format(data_file_path))
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
            
    stonks_utils.make_dir(data_file_path)
    
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
