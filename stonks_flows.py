#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    stonks_flows - contains a set of predefined flows using the stonks
    ETL libraries as examples and to define automated analytic flows
    

"""
import stonks_utils as su
import stonks_extract as se
import stonks_output as so

LOCAL_DATA_DIR = './datasets/'


# TO BE MOVED TO stonk_flow.py
# get all dividend histories from dividendhistory.org and save to provided file path
# in_file_path is the root dataset path with trailing '/' 
# other directories will be created in here so should be writable
def get_div_histories_DH(in_file_path):
    
    data_file_path = in_file_path
    
    for exc in su.MARKETS:
        ticks = se.get_tickers_divhistory(exc)
        div_path = data_file_path + f"{exc}/"
        i=0
        su.printProgressBar(0, len(ticks), prefix = f'{exc} Div History Progress:', suffix = 'Complete', length = 50)
        for sym in ticks: 
            i+=1
            su.printProgressBar(i, len(ticks), prefix = f'{exc} Div History Progress:', suffix = 'Complete', length = 50)
            dfs = se.get_div_history_DH(sym, exc)
            so.df_to_csv(dfs, div_path, f"DH_div_history_{sym}.csv", False)
    return su.SUCCESS
    
# flow used to get tickers and other info from divhistory
# kept as is for backward compatibility

def getTickers(in_file_path):
    data_file_path = in_file_path
    
    for exc in su.MARKETS:
        df = se.get_ticker_summary_divhistory(exc)
        if so.df_to_csv(df, data_file_path, f"DH_tickers_{exc}.csv", False)==su.FAILURE:
            print(f"Error writing DH_tickers_{exc}.csv")
            
    return su.SUCCESS