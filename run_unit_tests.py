#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run_unit_tests.py -- Collection of unit tests for all stonks modules and functions

"""
import stonks_extract as se


def main():
    
    # stonks_extact unit tests
    print(">>> stonks_extract Unit Tests")
    try:
        df = se.get_tickers_divhistory('tsx')
        assert(len(df) != 0)
        print("get_tickers - tsx test - Passed")
    except AssertionError:
        print("get_tickers - tsx test - Failed")
        
    try: 
        df = se.get_tickers_divhistory('nyse')
        assert(len(df) != 0)
        print("get_tickers - nyse test - Passed")
    except AssertionError:
        print("get_tickers - nyse test - Failed")
    
    try:
        df = se.get_tickers_divhistory('nasdaq')
        assert(len(df) != 0)
        print("get_tickers - nasdaq test - Passed")
    except AssertionError:
        print("get_tickers - nasdaq test - Failed")
    
    try:
        df = se.get_tickers_divhistory('nys')
        assert(df == -1)
        print("get_tickers - invalid string test - Passed")
    except AssertionError:
        print("get_tickers - invalid string test - Failed")
        
        
    

if __name__ == "__main__":
    main()