#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

stonks_transform - this library contains all transforms for analysis 

Transform functions should use pandas dataframe as primary input and output format
    
    
"""

import pandas as pd
import numpy as np
from scipy.signal import find_peaks
from pandas import DataFrame
import datetime

import stonks_utils as su

# inputs 3 dataframes from DH_div_history, DH_weekly_reports, yahoo_price_history
# outputs dataframe with yield history

def generate_yield_history(in_df_divs:pd.DataFrame, in_df_div_freqs:pd.DataFrame, in_df_prices:pd.DataFrame, in_ticker:str):
    
    in_df_div_freqs.drop(columns=["Name", "Price", "Yld", "Ex-Div", "PayRto", "PE", "PB", "Beta", "Mkt Cap", "WK%", "MO%", "2MO%", "3MO%", "6MO%", "1YR%", "report_date_epoch", "ex_div_epoch"], inplace=True)
    
    in_df_divs.rename(columns={'Ex-Dividend Date':'Date'}, inplace=True)
    result = pd.merge(in_df_divs, in_df_prices, on=['Date'], how='outer')
    result.sort_values(by='Date', inplace=True)
    result.fillna(method='ffill', inplace=True)
    result.drop(columns=['Open', 'High', 'Low', 'Dividends', 'symbol', 'market', 'date_epoch', 'Stock Splits'], inplace=True)
    
    try:
        # frequency factor
        freq = in_df_div_freqs.loc[in_df_div_freqs['Symbol'] == in_ticker]
        #print(freq)
        if freq.iloc[0]['div_freq'] == 'Q':
            yield_factor = 4
        elif freq.iloc[0]['div_freq'] == 'S':
            yield_factor = 2
        elif freq.iloc[0]['div_freq'] == 'M':
            yield_factor = 12
        elif freq.iloc[0]['div_freq'] == 'A':
            yield_factor = 1
        else:
            # ignoring U and - for now
            yield_factor = 0
    except:
        print("Error getting freq")
        return su.FAILURE
    
    
    # yield calculation
    result['Daily Yield'] = yield_factor*result['Cash Amount']/result['Close']
    # remove historic price records with no div
    result = result[result['Daily Yield'].notna()]
    
    return result

# model parameters
#    prom - prominence for peak detection
#    (optional) date_range - number of years to go back when building model (default=max)
#    (optional) std - remove data points outside in_std standard deviations is outlier_removal is specified
#
# return peak avg, valley avg, peaks array, valleys array

def generate_peak_model(in_df: DataFrame, *args, **kwargs):
    
    in_date_range = kwargs.get('date_range')
    in_std = kwargs.get('std')
    in_prom = kwargs.get('prom')
    
    if in_date_range != 'max':
        try:
            in_date_range = int(in_date_range)
        except ValueError:
            print("Value of date_range should either be an int or 'max'")
            return -1
        in_df = trim_by_date(in_df, years_back=in_date_range)
    
    if in_prom != None:
        try:
            in_prom = float(in_prom)
        except ValueError:
            print("Prominence value should be an float")
            return -1
    # default prominence level 
    else:
        in_prom = 0.004
    
    '''
     TO IMPLEMENT - std option to remove ouitliers
    '''
    
    # need a 0 based index for peaks 
    in_df = in_df.reset_index(drop=True)
    value_array = in_df['Daily Yield']
    #date_array = in_df['Date']
    
    peaks = find_peaks(value_array, prominence=in_prom)[0]
    valleys = find_peaks(-value_array, prominence=in_prom)[0]

    total = 0 
    for temp in peaks:
        total += value_array[temp] 
    
    peak_avg = total/len(peaks)
    #print(f"Peak Average value {peak_avg}")

    total =0 
    for temp in valleys:
        total += value_array[temp] 
    
    valley_avg = total/len(valleys)
    #print(f"Valley Average value {valley_avg}")
        
    return peaks, valleys, peak_avg, valley_avg
    
    
    
#assumes the dataframe passed has a column called Date for date boxing
# in_df - pandas Dataframe to trim
#
# start_date (NOT implemented) - datetime object for start date 
# (optional) end_date (NOT implemented) - datetime object for end-date (default is today)
# OR
# years_back (implemented) - in value for number of years to go back (startdate = 1 Jan in_years_back years ago)



def trim_by_date(in_df: DataFrame, *args, **kwargs):
    
    in_years_back = kwargs.get('years_back')
    in_start_date = kwargs.get('start_date')
    in_end_date = kwargs.get('end_date')
    
    if in_years_back != None:   
        try:
            in_years_back = int(in_years_back)
        except ValueError:
            print("Value of date_range should either be an int or 'max'")
            return -1
        now = datetime.datetime.now()
        start_date = datetime.datetime(now.year-in_years_back, 1, 1)
        end_date = now
        
    '''
        TO IMPLEMENT - Start and end date provided and trim
    '''    
        
    in_df['Date'] = pd.to_datetime(in_df['Date'])
    mask = (in_df['Date']> start_date) & (in_df['Date']<=end_date)
    
    new_df = in_df.loc[mask]
    new_df = new_df.reset_index(drop=True)
    
    return (new_df)
    
    

    