# stonks_ftw
A project to build a stock data pipeline and ML recommendation system.

I am using the project to learn about building data pipelines, data analysis using ELK stack, and building ML models for identifying stocks to consider for buy or sell based on some basic dividend value based investment formulas. For those interested, I am also keeping a journal of snags I hit, solutions found with sources, and other observations.

In this project I will keep my notes on building my data collector, any files needed to enable transformation and ingestion into an ELK system and/or DB to enable analysis, ML code for models I play with, and really anything else to enable a full stack datascience system for basic stock analysis.

I am taking on this project more as a learning experience than to make money but who knows? I may find some interesting things. For those interested, I am also keeping a journal of snags I hit, solutions found with sources, and other observations.

# Current state 

My collector code is in a pretty good state pulling in various datasets from dividendhistory.org and yahoo finance (using yfinance).  Daily yields are being calculated as part of initialization and some initial work on peak and valley detection has been done in notebook.  Next step is to optimize peak and valley detection to find optimal buy and sell points.  The model I am using to start is to average out peak and valley values for dividend yield to identify buy and sell points for all dividend stocks.  

# Future ideas
  - add in a postgres backend to get away from basing all workflows on text files
  - work on dash enabled dash board and plotly based visualizations
  - generate model files for each ticker offline using total and 10 year histories 
  - consider generating model on the fly to allow for parameter tuning
  - build an interface to dividendhistory data that is more consistent with yfinance python OO constructs.
  - add functionality to enable on demand data fetching (useful for alerting and updating recommendation model)
  - try adding functionality to provide buy, sell, hold query interface based on models
  - try exploring models for non-dividend stocks using basic ratios and metrics (from financials, PE history, PB history, etc)

# Initial sources to pull from

I have looked at a number of sources to pull financial information. There is no shortage of providers if you are willing to pay. Free accounts at many of the services that provide data through API have call ceilings that would make it very difficult to test and grab data as aggressively as I would like. The main site I am using, given my focus on dividend paying stocks to start, is dividendhistory.org. They provide historic dividend data based on ticker symbols, closing price, company name, PE, PB, and close price. They also provide weekly reports for all dividend paying stocks with lots of fundamental data that may be useful.

The main source I am looking at for daily ticker info and other financial data is yahoo finance through yfinance (https://github.com/ranaroussi/yfinance).

Other APIs I have looked at include the following:

API for quote data from Alpha Vantage (confirmed - TSE: append for Can quotes) - https://www.alphavantage.co/documentation/#time-series-data. Alpha Vantage also accessible through the pandas_datareader class directly.

# Tools created for this project
### stonk_utils.py
My collection of python code blocks to create my data set. Outputs data sets to csv for future processing in the pipeline. There is currently support for TSX, NYSE, and NASDAQ dividend stocks. Automatically creates directory sturcture in project directory or another user specified directory. Also prepares data for ingest into elasticsearch using logstash for follow-on use in Kibana.

Currently implemented:
grab ticker lists from dividendhistory.org
grab dividend payout history for each ticker from dividendhistory.org
grab weekly dividend stock reports (published on Fridays) from dividendhistory.org

### initialize.py
Initialization script to get the datasources setup. This script uses stonks_utils.py to create all the datasets supported.
usage: initialize.py [-f datasetpath [[default is project path]]]

If you receive an immediate "Could not get TSX ticks" error, it may be due to a missing python dependency that was not installed with pandas. Try ``pip3 install lxml``. 

### daily_collector.py
This is the daily collector meant to be run as an update script for all datasets.  The default behaviour is to update price, weekly report, and dividend history records from the date the last record was collected.  This can be run standalone to update exisitng datasets but it was designed to run inside a crontab daily to automatically update the dataset.  
```usage: daily_collector.py [-p --price, -d --div, -w --weekly]
  -p, --price:  updates daily price records from last record date
  -d, --div:  updates dividend history records (currently just redownloads the full set)
  -w, --weekly: updates weekly reports from dividendhistory.org 
```
Typical usage in a crontab is `daily_collector.py -p -w -d`

# Elasticstack setup
Currently the elasticsearch indexes need to be setup manually. I have found it easiest to run HTTP commands in Kibana DevTools.

A collection of useful HTTP elasticsearch queries are provided in the useful_elastic_queries.txt file.

There are 4 indexes used in this project for each of the current datasets.  Going forward, I will likely use a different backend for persistent storage but will continue to use elastic for monitoring and exploration.  

# Logstash ingest of ticker dataset to elasticsearch

## Running logstash manually to load dataset into elasticsearch
Once this is created, use the manual_logstash_load.config with logstash to load up the data in Elasticsearch. Right now it assumes that the Elasticstack components are all running locally. The following logstash command will load the data (uses the manual_logstash_load.config pipeline configuration provided in this project):

To test configuration files:
```
config test sudo /usr/share/logstash/bin/logstash --config.test_and_exit -f "/home/brad/projects/stonksftw/stonks_ftw/manual_logstash_load_tickers.config"
```
To load data using provided configs:
```
sudo /usr/share/logstash/bin/logstash -r -f "/home/brad/projects/stonksftw/stonks_ftw/manual_logstash_load_tickers.config"
```
The follwing configs can be used to setup ingest pipelines for dividend history records and weekly reports from dividendhistory.org and price history from yahoo finance (found in the logstash_pipeline_configs).  

* manual_logstash_load_div_history.config
* manual_logstash_load_DH_weekly.config
* manual_logstash_load_price_history.config

## Running logstash as a service to autoload data into elastic
You can run logstash as a service to automatically push dataset updates to elasticsearch by modifying the pipelines.yml file and adding the configs in the pipelines directory from this project and starting the logstash service.  Running in this configuration in combination with running the daily_collector.py as a cron job will create a regularly updated data collection pipeline for all supported financial datasets.  More details on setting up logstash as a service for this project can be found at: https://github.com/bradmetz/stonks_ftw/wiki/Tips-on-moving-from-Logstash-run-once-using--f-config-to-running-as-a-service

# Kibana index setup
To get Kibana to recognize the data, create an index in the Kibana management panel for stonks. Use the ex_div_date_snap_epoch as main time series field. The epoch timestamp will allow Kibana to properly display and process the ex-div_snap field.

For the DH Weekly reports in , I recommend using the report_date_epoch as the main time series field when you setup your index.  This will make creation of future visualizations easier.  

For dividend history records, I recommend using the ex-div date as the main time series field in the kibana index. 

# Initial playing with python packaging

If you want to try and download and install the latest version of stonksftw, grab it from this link
https://test.pypi.org/project/stonksftw-pkg-bradmetz/0.0.1/

# Next steps  
* explore kafka and/or redis
* look at generalizing the data pipeline creation framework.
* alerting on specific conditions
* daily reports on what is coming up
* bokeh or dash for visualization

# Readings for future tasks
Peak detection example for extracting max div values: https://stackoverflow.com/questions/1713335/peak-finding-algorithm-for-python-scipy

Elasticsesarch-py reference and project: https://github.com/elastic/elasticsearch-py
