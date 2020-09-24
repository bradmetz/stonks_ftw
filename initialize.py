#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
initialization script grabs all ticker symbols from TSX, NASDAQ, and NYSE 
that pay a dividend based on dividendhistory.org

standalone run once script

can be run with no parameters

"""
import sys, getopt
import pandas as pd
import stonks_utils
import stonks_flows as sf

def main():
    
    global data_file_path
    data_file_path = "./datasets/"
    parse_args()
    
    sf.getTickers(data_file_path)
    sf.get_div_histories_DH(data_file_path)
    
    #stonks_utils.get_div_histories_DH(data_file_path)
    
    stonks_utils.dl_and_write_DH_reports(data_file_path, "USA", year=2019)
    stonks_utils.dl_and_write_DH_reports(data_file_path, "CAN", year=2019)
    
    # need to pass tickers as a list
    dfs = pd.read_csv('./datasets/DH_tickers_tsx.csv', keep_default_na=False)
    sym_list = dfs['Symbol'].to_list()
    stonks_utils.get_ticker_price_history(sym_list, 'max', data_file_path, 'TSX')
    stonks_utils.get_all_div_yield_histories(sym_list, 'tsx', data_file_path)

    dfs = pd.read_csv('./datasets/DH_tickers_nyse.csv', keep_default_na=False)
    sym_list = dfs['Symbol'].to_list()
    stonks_utils.get_ticker_price_history(sym_list, 'max', data_file_path, 'NYSE')
    stonks_utils.get_all_div_yield_histories(sym_list, 'nyse', data_file_path)
    
    dfs = pd.read_csv('./datasets/DH_tickers_nasdaq.csv', keep_default_na=False)
    sym_list = dfs['Symbol'].to_list()
    stonks_utils.get_ticker_price_history(sym_list, 'max', data_file_path, 'NASDAQ')
    stonks_utils.get_all_div_yield_histories(sym_list, 'nasdaq', data_file_path)

def parse_args():
    global data_file_path
    try:
        opts, args = getopt.getopt(sys.argv[1:], "t:hef", ["help", "elastic", "file", "temp="])
    except getopt.GetoptError:
        usage()
    #print(f"opts entered{opts}")
    #print(f"args entered{args}")
    for o, a in opts:
        if o in ("-e", "--elastic"):
            print('Elastic option selected')
        if o in ("-t", "--temp"):
            data_file_path = str(a)
            print("Data file path: {}".format(data_file_path))
        if o in ("-h", "--help"):
            usage()
    stonks_utils.make_dir(data_file_path)
    
def usage():
    print ('-----------------------------------------------------------')
    print ('Initialization script for stonksftw stock analysis project')
    print ('Usage: initialize.py [-e|-f|-t] ')
    print ('-e --elastic : load tickers direct to elastic')
    print ('')
    print ('-t --temp : specify temp directory to store tickers prior to elastic load (default is <projectdir>/datasets')
    print ('')
    
    print ('-----------------------------------------------------------')
    sys.exit(' ')


if __name__ == "__main__":
    main()

