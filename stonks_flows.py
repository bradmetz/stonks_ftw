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


# flow used to get tickers and other info from divhistory
# kept as is for backward compatibility

def getTickers(in_file_path):
    data_file_path = in_file_path
    
    for exc in su.MARKETS:
        df = se.get_ticker_summary_divhistory(exc)
        if so.df_to_csv(df, data_file_path, f"DH_tickers_{exc}.csv")==su.FAILURE:
            print(f"Error writing DH_tickers_{exc}.csv")
        
    #df.to_csv(f'{data_file_path}DH_tickers_tsx.csv')
    
    #df = se.get_tickers_divhistory('nyse')
    #if so.df_to_csv(df, data_file_path, "DH_tickers_nyse.csv")==su.FAILURE:
    #    print("Error writing DH_tickers_nyse.csv")
    
    
    #df.to_csv(f'{data_file_path}DH_tickers_nyse.csv')
    
    #df = se.get_tickers_divhistory('nasdaq')
    #if so.df_to_csv(df, data_file_path, "DH_tickers_nasdaq.csv")==su.FAILURE:
    #    print("Error writing DH_tickers_nasdaq.csv")
        
    return su.SUCCESS