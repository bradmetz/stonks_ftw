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
    
    # TSX dividend history download 
    dfs = pd.read_csv(f'{data_file_path}pandas_div_history_tsx.csv', keep_default_na=False)
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
            df.iloc[2:, :-1].to_csv(f'{div_path}pandas_div_history_{sym}.csv', index=False)
    
    # NYSE dividend history download
    dfs = pd.read_csv(f'{data_file_path}pandas_div_history_nyse.csv', keep_default_na=False)
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
            df.iloc[2:, :-1].to_csv(f'{div_path}pandas_div_history_{sym}.csv', index=False)
    
    # NASDAQ dividend history download
    dfs = pd.read_csv(f'{data_file_path}pandas_div_history_nasdaq.csv', keep_default_na=False)
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
            df.iloc[2:, :-1].to_csv(f'{div_path}pandas_div_history_{sym}.csv', index=False)
    
    
    
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
    make_dir(data_file_path)
    
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

