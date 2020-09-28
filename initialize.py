#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
initialization script grabs all ticker symbols from TSX, NASDAQ, and NYSE 
that pay a dividend based on dividendhistory.org

standalone run once script

can be run with no parameters

"""
import sys #, getopt
#import pandas as pd
#import stonks_utils
import stonks_flows as sf
import stonks_extract as se
import stonks_utils as su

LOCAL_DATASET_PATH = "./datasets/"

def main():
    
    sf.getTickers(LOCAL_DATASET_PATH)
    sf.get_div_histories_DH(LOCAL_DATASET_PATH)
    
    dh_reports_path = LOCAL_DATASET_PATH + 'weekly_divhistory_reports/'
    sf.dl_and_write_DH_reports(dh_reports_path, "nyse", year=2019)
    sf.dl_and_write_DH_reports(dh_reports_path, "tsx", year=2019)
    
    for exc in su.MARKETS:
        sym_list = se.get_tickers_divhistory(exc)
        sf.get_ticker_price_history(sym_list, LOCAL_DATASET_PATH + "price_history/", exc)
    
    #sym_list = se.get_tickers_divhistory('nyse')
    #sf.get_ticker_price_history(sym_list, LOCAL_DATASET_PATH + "price_history", 'nyse')
    
    #sym_list = se.get_tickers_divhistory('nasdaq')
    #sf.get_ticker_price_history(sym_list, LOCAL_DATASET_PATH + "price_history", 'nasdaq')
    
    return se.SUCCESS
    
def usage():
    print ('-----------------------------------------------------------')
    print (" ")
    print ('Initialization script for stonksftw stock analysis project')
    print (" ")
    print ('-----------------------------------------------------------')
    sys.exit(0)


if __name__ == "__main__":
    main()

