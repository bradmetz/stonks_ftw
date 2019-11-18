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

# ELK stack setup initial thoughts

I got my ELK stack up and running which has allowed me to learn a bit about the setup and administration of the core ELK stack components.  Aside from some errors due to trying to get setup on old hardware (note:  ML components in Elasticsearch require SSE4.2 instruction set support) I am up and running on my lubuntu image.  

Based on my initial thinking in my data collection so far, I am going to try and setup a Logstash pipeline to ingest my collected data into my Elastic instance.  Other options included pushing the updates straight to Elastic using curl (or likely a python HTTP client API), or building my own Beats data shipper.  For proof of concept it looks like logstash pipeline is the quickest route to success. 

Started playing with Elasticsearch getting indices setup.  The following can be used to create indices to use with the project using curl:

Create index for companies
curl -XPUT 'http://192.168.0.20:9200/stonks_ftw' -H 'Content-Type: application/json' -d'{"settings" : {"index" : {"number_of_shards" : 1, "number_of_replicas" : 0}}}'

Map fields in companies type
curl -XPUT 'http://192.168.0.20:9200/stonks_ftw/companies/_mapping?include_type_name=true' -H 'Content-Type: application/json' -d @"create_company_schema.json"

Wrote up python code to populate my companies type with data scraped from each market table on dividendhistory.org.  Now need to populate dividend histories for each company.  

Next step:  Give some thought for how to present the data to the pipeline from the collector to get into Elastic.  Initial thinking is to ingest daily closing price with dividend yield calculated based on collected current dividends.  This would mean creating a pipeline for each ticker symbol (since current flow dumps price history for each ticker into their own file).  Better option for pipeline maybe to have a single file with ticker as a field.  

# References
Neat looking webscraper - simple scraper.io
