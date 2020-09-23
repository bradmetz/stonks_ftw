#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    stonks_flows - contains a set of predefined flows using the stonks
    ETL libraries as examples and to define automated analytic flows
    

"""
import stonks_utils as su
import stonks_extract as se
import stonks_output as so


# flow used to get tickers and other info from divhistory
# kept as is for backward compatibility

def getTickers(in_file_path):
    data_file_path = in_file_path
    
    df = se.get_tickers_divhistory('tsx')
    if so.df_to_csv(df, data_file_path, "DH_tickers_tsx.csv")==su.FAILURE:
        print("Error writing DH_tickers_tsx.csv")
        
    #df.to_csv(f'{data_file_path}DH_tickers_tsx.csv')
    
    df = se.get_tickers_divhistory('nyse')
    if so.df_to_csv(df, data_file_path, "DH_tickers_nyse.csv")==su.FAILURE:
        print("Error writing DH_tickers_nyse.csv")
    
    
    #df.to_csv(f'{data_file_path}DH_tickers_nyse.csv')
    
    df = se.get_tickers_divhistory('nasdaq')
    if so.df_to_csv(df, data_file_path, "DH_tickers_nadaq.csv")==su.FAILURE:
        print("Error writing DH_tickers_nasdaq.csv")
        
    return su.SUCCESS