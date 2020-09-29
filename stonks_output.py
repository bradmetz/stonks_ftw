#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    stonks_output.py - module for writing out stonks DFs to various systems
    
    Version 0.1
    - support for output to csv with option to create directory
    

"""
import pandas as pd
import stonks_utils as su

# safely create directory, write check, and write out
# Used to write out a data frame to csv for later use

def df_to_csv(in_df:pd.DataFrame, in_path, in_file_name, keep_index):
        
    if su.make_dir(in_path)==su.SUCCESS:
        try:
            in_df.to_csv(f'{in_path}{in_file_name}', index=keep_index)
        except PermissionError:
            print("Permission error on file write")
            return su.FAILURE
    return su.SUCCESS 

def append_df_to_csv(in_df:pd.DataFrame, in_path, in_file_name):
    
    try:
        in_df.to_csv(f'{in_path}{in_file_name}', mode='a', index=False, header=False)
    except PermissionError:
        print("Permission error on file write")
        return su.FAILURE
    return su.SUCCESS 