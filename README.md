# stonks_ftw
A project to build a stock data pipeline and ML recommendation system.

I am using the project to learn about building data pipelines, data analysis using ELK stack, and building ML models for identifying stocks to consider for buy or sell based on some basic dividend value based investment formulas.  
In this project I will keep my notes on building my data collector, any files needed to enable transformation and ingestion into an ELK system and/or DB to enable analysis, ML code for models I play with, and really anything else to enable a full stack datascience system for basic stock analysis.

I am taking on this project more as a learning experience than to make money but who knows?  I may find some interesting things.

# Initial sources to pull from

Historic Dividend data based on ticker symbols.  Also provides PE, PB, close price - dividendhistory.org
API for quote data from Alpha Vantage (confirmed - TSE: append for Can quotes) - https://www.alphavantage.co/documentation/#time-series-data
Alpha Vantage also accessible through the pandas_datareader class directly.

# Tools created for this project

collector.py - My collection of python code blocks to create my data set.  Outputs my data sets to csv for future processing in the pipeline.  I have also left my dead end code blocks in there as well.  There is currently support for TSX, NYSE, and NASDAQ.  File structure needs to be created manually (may add support to automatically create this in the future).  
I thought about pulling down price on day of dividend payment for each ticker but with the call limits on Alpha Vanatage may make pulling down full histories a better option. Will look at adding a collector for histories first. 

# References
Neat looking webscraper - simple scraper.io
