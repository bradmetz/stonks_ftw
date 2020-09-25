#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run_unit_tests.py -- Collection of unit tests for all stonks modules and functions

"""
import stonks_extract as se
import stonks_utils as su
import datetime


def main():
    
    # stonks_extact unit tests
    print(">>> stonks_extract Unit Tests")
    try:
        df = se.get_ticker_summary_divhistory('tsx')
        assert(len(df) != 0)
        print("get_ticker_summary_DH - tsx test - Passed")
    except AssertionError:
        print("get_ticker_summary_DH - tsx test - Failed")
        
    try: 
        df = se.get_ticker_summary_divhistory('nyse')
        assert(len(df) != 0)
        print("get_ticker_summary_DH - nyse test - Passed")
    except AssertionError:
        print("get_ticker_summary_DH - nyse test - Failed")
    
    try:
        df = se.get_ticker_summary_divhistory('nasdaq')
        assert(len(df) != 0)
        print("get_ticker_summary_DH - nasdaq test - Passed")
    except AssertionError:
        print("get_ticker_summary_DH - nasdaq test - Failed")
    
    try:
        df = se.get_ticker_summary_divhistory('nys')
        assert(df == -1)
        print("get_ticker_summary_DH - invalid string test - Passed")
    except AssertionError:
        print("get_ticker_summary_DH - invalid string test - Failed")
        
    try:
        df = se.get_tickers_divhistory('nyse')
        assert(type(df) == list)
        print("get_tickers - list return test - Passed")
    except AssertionError:
        print("get_tickers - list return test - Failed")
        
        
        
    print(">>> DH Weekly report tests")    
        
    try:
        
        date_str  = "2020-09-18"
        in_date = datetime.date.fromisoformat(date_str)
        #in_date = datetime.datetime.strptime(date_str, "%Y-%m-%d"
        df = se.get_DH_weekly_report('nyse', in_date)
        assert(len(df) != 0)
        print("DH weekly report - df nyse return test - Passed")
    except AssertionError:
        print("DH weekly report - df nyse return test - Failed")
        
    try:
        
        date_str  = "2020-09-24"
        in_date = datetime.date.fromisoformat(date_str)
        #in_date = datetime.datetime.strptime(date_str, "%Y-%m-%d"
        df = se.get_DH_weekly_report('nyse', in_date)
        assert(df == su.FAILURE)
        print("DH weekly report - not Friday test - Passed")
    except AssertionError:
        print("DH weekly report - not Friday test - Failed")
    
    try:
        
        date_str  = "2020-09-18"
        in_date = datetime.date.fromisoformat(date_str)
        #in_date = datetime.datetime.strptime(date_str, "%Y-%m-%d"
        df = se.get_DH_weekly_report('tsx', in_date)
        assert(len(df) != 0)
        print("DH weekly report - tsx test - Passed")
    except AssertionError:
        print("DH weekly report - tsx test - Failed")
        
    try:
        
        date_str  = "2020-09-18"
        in_date = datetime.date.fromisoformat(date_str)
        #in_date = datetime.datetime.strptime(date_str, "%Y-%m-%d"
        df = se.get_DH_weekly_report('ts', in_date)
        assert(df == su.FAILURE)
        print("DH weekly report - invalid market test - Passed")
    except AssertionError:
        print("DH weekly report - invalid market test - Failed")
    
    print(">>> Yahoo Price History per ticker tests")    
        
    try:
        df = se.get_ticker_price_history_yahoo('AAPL', 'nasdaq', 'max')
        assert(len(df) != 0)
        print("Yahoo Price history - df AAPL nasdaq return test - Passed")
    except AssertionError:
        print("Yahoo Price history - df AAPL nasdaq return test - Failed")
        
    try:
        df = se.get_ticker_price_history_yahoo('AAPL', 'nyse', 'max')
        assert(df == su.FAILURE)
        print("Yahoo Price history - mismatched ticker/market test - Passed")
    except AssertionError:
        print("Yahoo Price history - mismatched ticker/market test - Failed")

    try:
        start_date_str  = "2010-09-18"
        df = se.get_ticker_price_history_yahoo('ATD.B', 'tsx', 'spec', in_start=start_date_str )
        assert(len(df) != 0)
        assert(('2009-01-01' in df['Date']) is False)
        print("Yahoo Price history - . ticker and TSX and spec test - Passed")
    except AssertionError:
        print("Yahoo Price history - . ticker and TSX and spec test - Failed")

if __name__ == "__main__":
    main()