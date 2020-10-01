#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

stonks_utils - a collection of general functions used across modules
    Helper functions to deal with dates (default class for dates is 
                                         datetime.date())

"""

import pandas as pd
import calendar, datetime, os, sys
import numpy as np
import yfinance as yf
from datetime import date
from dateutil.relativedelta import relativedelta, FR
import stonks_utils as su
# Globals for use across operations

SUCCESS = 0
FAILURE = -1
MARKETS = ('tsx', 'nyse', 'nasdaq')
   
# in_country is either CAN or USA
# TO REFACTOR - generalize for local store anywhere (from csv) and add to 
#    stonks_extract
# returns a date object

def get_last_weekly_report_date(in_country, in_path):
    
    if in_country!='USA' and in_country!='CAN':
        print("in_country must be one of CAN or USA")
        return su.FAILURE
    try: 
        dates = os.listdir(f'{in_path}{in_country}')
    except FileNotFoundError:
        print(f"Dir {in_path}{in_country} not found")
        return su.FAILURE
    
    dates = [item.lstrip(f'div_history_report-{in_country}-') for item in dates]
    dates = [item.rstrip('.csv') for item in dates]
    dates_list = [datetime.datetime.strptime(date, '%Y-%m-%d').date() for date in dates]
    maxdate = max(dates_list)
    return maxdate
    
# returns an array of date objects of all fridays from the year given 
# to the last Friday from the current day
# use in_year=2019 - this is used for dataset initialization

def all_fridays_from(in_year):
    
    temp_year = in_year #kwargs.get('in_year')
    #pdate_flag = kwargs.get('update')
    #in_market = kwargs.get('in_market')
    #print(f"in_year: {temp_year}  update: {update_flag}  in_market: {in_market}")
    fridays = []
    if temp_year!=None and temp_year>2018:
        current_date = datetime.datetime.now()
        for year in range(temp_year, current_date.year+1):
            for month in range (1, 13):
                cal = calendar.monthcalendar(year, month)
                for week in cal:
                    if week[calendar.FRIDAY] != 0:
                        x = datetime.datetime(year, month, week[calendar.FRIDAY])
                        if x<current_date:
                            fridays.append(x.date())
    return fridays
   
# assumes that DH reports are stored with directories for each country
# returns     

def fridays_since_last_DH_report(in_data_path, in_market):
    
    if in_market in ('nyse', 'nasdaq'):
        in_country = 'USA'
    elif in_market == 'tsx':
        in_country = 'CAN'
    elif in_market in ('CAN', 'USA'):
        in_country = in_market
    else:
        print(f"{in_market} is not a valid market value")
        return []
    fridays = []
    
    temp_date = get_last_weekly_report_date(in_country, in_data_path)
    if temp_date == FAILURE:
        print(f"Error finding last report: {in_data_path} {in_market}")
        return []
    while temp_date<datetime.datetime.today().date():
        temp_date = next_weekday(temp_date, 4)
        if temp_date>datetime.datetime.today().date():
            #print(f"{temp_date} - Failed")
            break
        fridays.append(temp_date)
        
    return fridays

# helper function to test for Friday

def is_friday(in_date:date):
    if in_date.isoweekday() == 5:
        return True
    return False

# returns date
def next_weekday(d, weekday):
    days_ahead = weekday - d.weekday()
    if days_ahead <= 0: # Target day already happened this week
        days_ahead += 7
    return (d + datetime.timedelta(days_ahead))

def get_last_friday():
    return date.today() + relativedelta(weekday=FR(-1))   

# assumes a date format YYYY-MM-DD 
def str_date_to_epoch(in_date_str):
    date_epoch = datetime.datetime.strptime(in_date_str, "%Y-%m-%d")
    return date_epoch.timestamp()

# returns 0 on success and -1 on error
def make_dir(path):
    if not os.path.exists(path):
        try:
            os.makedirs(path)
            print(f"Directory {path} created")
        except PermissionError:
            print(f"Permission to create directory {path} DENIED ... quitting.")
            return FAILURE
    return SUCCESS
        
# Print iterations progress
# taken from stack overflow: https://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()