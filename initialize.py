#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
initialization script grabs all ticker symbols from TSX, NASDAQ, and NYSE 
that pay a dividend based on dividendhistory.org

standalone run once script
"""
import sys, getopt, os, progressbar
import pandas as pd

def main():
    global data_file_path
    data_file_path = "./datasets/"
    parse_args()
    getTickers()
    
    
    dfs = pd.read_csv(f'{data_file_path}pandas_div_history_tsx.csv', keep_default_na=False)
    ticks = dfs.iloc[:, 1:2]

    # loop throuigh all tickers and create new csv for each div stock


    bar = progressbar.ProgressBar(maxval=20, widgets=["TSX Dividends from dividendhistory.org", progressbar.Bar('=', '|', '|',' ', progressbar.Percentage())])
    bar.start()
    for (sym_index, sym_val) in ticks.iteritems():
    #cycle through all tickers and pull down div history and store in data folder
        for sym in sym_val.values:
            #needed to deal with '.'s in ticker symbols (eg ATB.B)
            sym = sym.replace('.', '_')
            print("https://dividendhistory.org/payout/{0}".format(sym))
            dfs = pd.read_html('https://dividendhistory.org/payout/{0}/'.format(sym))

    # small decision block to deal with optional anoucements header on some pages
            if len(dfs)==3:
                df = dfs[0]
            elif len(dfs)==4:
                df = dfs[1]
            else:
                print('something else going on here')
# dropthe first two rows since they are unconfirmed
# drop the last column (i can calculate div increase percentages myself) 
    #        dfout = df.iloc[2:, :-1]
            df.iloc[2:, :-1].to_csv('./datasets/ind_div_history/nyse/pandas_div_history_{0}.csv'.format(sym))
    bar.finish()
    
    
    
    
    
def getTickers():
    bar = progressbar.ProgressBar(maxval=20, widgets=["TSX Tickers", progressbar.Bar('=', '|', '|',' ', progressbar.Percentage())])
    bar.start()
    dfs = pd.read_html('https://dividendhistory.org/tsx', keep_default_na=False, header=0, index_col=0)
    df = dfs[0]
    df.to_csv(f'{data_file_path}pandas_div_history_tsx.csv')
    bar.finish()
    
    bar = progressbar.ProgressBar(maxval=20, widgets=["NYSE Tickers", progressbar.Bar('=', '|', '|',' ', progressbar.Percentage())])
    bar.start()
    dfs = pd.read_html('https://dividendhistory.org/nyse', keep_default_na=False, header=0, index_col=0)
    df = dfs[0]
    df.to_csv(f'{data_file_path}pandas_div_history_nyse.csv')
    bar.finish()

    bar = progressbar.ProgressBar(maxval=20, widgets=["NASDAQ Tickers", progressbar.Bar('=', '|', '|',' ', progressbar.Percentage())])
    bar.start()
    dfs = pd.read_html('https://dividendhistory.org/nasdaq', keep_default_na=False, header=0, index_col=0)
    df = dfs[0]
    df.to_csv(f'{data_file_path}pandas_div_history_nasdaq.csv')
    bar.finish()
    


def parse_args():
    global data_file_path
    try:
        opts, args = getopt.getopt(sys.argv[1:], "t:hef", ["help", "elastic", "file", "temp="])
    except getopt.GetoptError:
        usage()
    print(f"opts entered{opts}")
    print(f"args entered{args}")
    for o, a in opts:
        if o in ("-e", "--elastic"):
            print('Elastic option selected')
        if o in ("-t", "--temp"):
            data_file_path = str(a)
            print("Data file path: {}".format(data_file_path))
        if o in ("-h", "--help"):
            usage()
            

    if not os.path.exists(data_file_path):
        try:
            os.makedirs(data_file_path)
            print(f"Directory {data_file_path} created")
        except PermissionError:
            print(f"Permission to create directory {data_file_path} DENIED ... quitting.")
            sys.exit(1)
    else:
        print(f"Directory {data_file_path} already exists ... going to use it for temp ticker store")

        
    



def usage():
    print ('-----------------------------------------------------------')
    print ('Initialization script for stonksftw stock analysis project')
    print ('Usage: initialize.py [-e|-f|-t] ')
    print ('-e --elastic : load tickers direct to elastic')
    print ('')
    print ('-t --temp : specify temp directory to store tickers prior to elastic load (default is <projectdir>/datasets')
    print ('-----------------------------------------------------------')
    sys.exit(' ')


if __name__ == "__main__":
    main()

