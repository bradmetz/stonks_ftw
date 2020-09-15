#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate and save out default models based on peak/valley averages for all
tickers and save to peak model directory in datasets

"""
import sys, getopt
import pandas as pd
import stonks_utils
import stonks_transform as st

def main():
    
    global data_file_path
    data_file_path = "./datasets/"
    stonks_utils.make_dir('./datasets/models/peaks_10_year/')
    stonks_utils.make_dir('./datasets/models/peaks_no_limit/')
    #parse_args()
    
    gen_and_save_model('tsx', './datasets/models/peaks_no_limit/')
    gen_and_save_model('nyse', './datasets/models/peaks_no_limit/')
    gen_and_save_model('nasdaq', './datasets/models/peaks_no_limit/')

    return 0

def gen_and_save_model(in_market, in_dataset_path):
    
    dfs = pd.read_csv(f'./datasets/DH_tickers_{in_market}.csv', keep_default_na=False)
    sym_list = dfs['Symbol'].to_list()
    output_df = []
    
    for curr_sym in sym_list:
        try:
            dfs2 = pd.read_csv(f'./datasets/yield_history/yield_history_{in_market}_{curr_sym}.csv')
            results = st.generate_peak_model(dfs2, date_range='max')
            output_df.append([curr_sym, in_market, results[2], results[3]])
            #print (curr_sym)
        except:
            print (f"No yield file for {curr_sym}")
            pass
            
    dfs2 = pd.DataFrame(output_df, columns=['Symbol', 'Market', 'Peak Avg', 'Valley Avg'])
    dfs2.to_csv(f'{in_dataset_path}{in_market}.csv', index=False)
    return 0

def parse_args():
    global data_file_path
    try:
        opts, args = getopt.getopt(sys.argv[1:], "t:hef", ["help", "elastic", "file", "temp="])
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
    print ('Generate and save out default models based on peak/valley averages for all')
    print ('tickers and save to peak model directory in datasetsInitialization script ')
    print ('for stonksftw stock analysis project')
    print (' ')
    print ('Usage: generate_peak_models.py ')
    print ('-----------------------------------------------------------')
    sys.exit(' ')


if __name__ == "__main__":
    main()

