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
import stonks_extract as se

LOCAL_DATASET_PATH = "./datasets/"

def main():
    
    #global data_file_path
    #data_file_path = "./datasets/"
    #parse_args()
    
    sf.getTickers(LOCAL_DATASET_PATH)
    sf.get_div_histories_DH(LOCAL_DATASET_PATH)
    
    dh_reports_path = LOCAL_DATASET_PATH + 'weekly_divhistory_reports/'
    sf.dl_and_write_DH_reports(dh_reports_path, "nyse", year=2019)
    sf.dl_and_write_DH_reports(dh_reports_path, "tsx", year=2019)
    
    
    # need to pass tickers as a list
    #dfs = pd.read_csv('./datasets/DH_tickers_tsx.csv', keep_default_na=False)
    #sym_list = dfs['Symbol'].to_list()
    
    sym_list = se.get_tickers_divhistory('tsx')
    
    stonks_utils.get_ticker_price_history(sym_list, 'max', data_file_path, 'TSX')
    stonks_utils.get_all_div_yield_histories(sym_list, 'tsx', data_file_path)


    sym_list = se.get_tickers_divhistory('nyse')
    #dfs = pd.read_csv('./datasets/DH_tickers_nyse.csv', keep_default_na=False)
    #sym_list = dfs['Symbol'].to_list()
    stonks_utils.get_ticker_price_history(sym_list, 'max', data_file_path, 'NYSE')
    stonks_utils.get_all_div_yield_histories(sym_list, 'nyse', data_file_path)
    
    sym_list = se.get_tickers_divhistory('nasdaq')
    #dfs = pd.read_csv('./datasets/DH_tickers_nasdaq.csv', keep_default_na=False)
    #sym_list = dfs['Symbol'].to_list()
    stonks_utils.get_ticker_price_history(sym_list, 'max', data_file_path, 'NASDAQ')
    stonks_utils.get_all_div_yield_histories(sym_list, 'nasdaq', data_file_path)

#def parse_args():
 ##  try:
   #     opts, args = getopt.getopt(sys.argv[1:], "t:hef", ["help", "elastic", "file", "temp="])
   ##3   usage()
    #print(f"opts entered{opts}")
    #print(f"args entered{args}")
    #for o, a in opts:
    #    if o in ("-e", "--elastic"):
    #        print('Elastic option selected')
    #    if o in ("-t", "--temp"):
    #        data_file_path = str(a)
    #        print("Data file path: {}".format(data_file_path))
    #    if o in ("-h", "--help"):
    #        usage()
    #stonks_utils.make_dir(data_file_path)
    
def usage():
    print ('-----------------------------------------------------------')
    print (" ")
    print ('Initialization script for stonksftw stock analysis project')
    print (" ")
    print ('-----------------------------------------------------------')
    sys.exit(0)


if __name__ == "__main__":
    main()

