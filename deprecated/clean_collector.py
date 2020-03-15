#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 20:46:13 2019

@author: Brad Metz
"""

# so after fighting with building an HTML parser to extact the TSX dividend
# from dividendhsitory.org, i found the method in pandas to pull down an
# HTML doc and parse all the tables into pandas data frames
# for this page the dataframe i want is the first (so index 0)
# the rest can be discarded

import pandas as pd
dfs = pd.read_html('https://dividendhistory.org/tsx', keep_default_na=False, header=0, index_col=0)
df = dfs[0]
df.to_csv('./datasets/pandas_div_history_tsx.csv')

# repeat to pull down the NYSE dividend stock list

#import pandas as pd
#dfs = pd.read_html('https://dividendhistory.org/nyse')
#df = dfs[0]
#df.to_csv('./datasets/pandas_div_history_nyse.csv')

# repeat to pull down the Nasdaq stock list

#import pandas as pd
#dfs = pd.read_html('https://dividendhistory.org/nasdaq')
#df = dfs[0]
#df.to_csv('./datasets/pandas_div_history_nasdaq.csv')

# basic code to pulldown dividend history based on stock ticker symbol
# TODO - Loop it through all tickers from previous step to popluate all
# dividend history data points.

import pandas as pd

# load tickers from previous summary csv
#tried loc with header 'Symbol'.  got errors finding Symbol
# not sure why but switched to integer index instead
# little quirk = kee_default_na needed to prevent the ticker value NA
# from being converted into an nan
dfs = pd.read_csv('./datasets/pandas_div_history_tsx.csv', keep_default_na=False, header=0, index_col=0)
ticks = dfs.index.values

#ticks = dfs.iloc[:, 1:2]
#list(ticks.columns.tolist())

##   print(col)

# loop throuigh all tickers and create new csv for each div stock
import numpy as np
for sym in dfs.index.values:

    sym = sym.replace('.', '_')
    print("https://dividendhistory.org/payout/tsx/{0}".format(sym))
    if (sym == "Symbol"):
        continue
    dfs = pd.read_html('https://dividendhistory.org/payout/tsx/{0}/'.format(sym))

# small decision block to deal with optional anoucements header on some pages
    if len(dfs)==3:
        df = dfs[0]
    elif len(dfs)==4:
        df = dfs[1]
    else:
        print('something else going on here')
# dropthe first two rows since they are unconfirmed
# drop the last column (i can calculate div increase percentages myself)
    dfout = df.iloc[2:, :-1]
    df.iloc[2:, :-1].to_csv('./datasets/ind_div_history/tsx/pandas_div_history_{0}.csv'.format(sym))
