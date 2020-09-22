# -*- coding: utf-8 -*-
"""
stonks_dash_app.py

Description:  Base script for Stonks web based dashboard.  This will be the 
main script for all visualizations and widgets for tuning. 

"""

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from pandas import DataFrame
import plotly.graph_objects as go
import numpy as np
from scipy.signal import find_peaks
import dash_bootstrap_components as dbc

# pass dataframe 

def generate_ticker_card(in_ticker, in_market):
    out_card = html.Div(
        dbc.Card(
            dbc.CardBody(
                [
                    html.H5(f"Ticker:  {in_ticker}", className='card-title'),
                    html.P([
                            "Company Name: "
                            ],
                        className='card-text',            
                    ),
                    html.P(["Price: 1 MILLION DOLLARS"], className='card-text',),
                    html.P(["Recommendation: SELL"], className='card-text',)
                ]
            ),  
        )   
    )

    return out_card

# pass a dataframe with same schema as yield_history dataset

def generate_yield_graph_from_df(in_df:DataFrame):
    

    dfs = in_df  #pd.read_csv(f'{in_home_path}datasets/yield_history/yield_history_{in_market}_{in_ticker}.csv')
    value_array = dfs['Daily Yield']
    date_array = dfs['Date']
 
    colors = {
        'background': '#111111',
        'text': '#7FDBFF'
        }
   
    peaks = find_peaks(value_array, prominence=0.003)[0]
    valleys = find_peaks(-value_array, prominence=0.003)[0]

    fig = go.Figure()
    #fig.layout.plot_bgcolor = colors['background']
    
    fig.add_trace(go.Scatter(
        x=date_array, 
        y=value_array,
        mode='lines+markers',
        name='Dividend Yield'
        ))

    fig.add_trace(go.Scatter(
        x=[date_array[i] for i in peaks],
        y=[value_array[j] for j in peaks],
        mode='markers',
        marker=dict(
            size=8,
            color='green',
            symbol='cross'
            ),
        name='Detected Peaks'
        ))

    fig.add_trace(go.Scatter(
        x=[date_array[i] for i in valleys],
        y=[value_array[j] for j in valleys],
        mode='markers',
        marker=dict(
            size=8,
            color='red',
            symbol='cross'
            ),
        name='Detected Valleys'
        ))

    total =0 
    for temp in peaks:
        total += value_array[temp] 
    
    peak_avg = total/len(peaks)
    print(f"Peak average value (total data set) {peak_avg}")

    total =0 
    for temp in valleys:
        total += value_array[temp] 
    
    valley_avg = total/len(valleys)
    print(f"Vally average value (total data set) {valley_avg}")

    peak_avg_list = [peak_avg]*len(dfs.index)
    valley_avg_list = [valley_avg]*len(dfs.index)

    fig.add_trace(go.Scatter(
        x=date_array, 
        y=peak_avg_list,
        mode='lines',
        name='Buy Threshold'
        ))
    
    
    fig.add_trace(go.Scatter(
        x=date_array, 
        y=valley_avg_list,
        mode='lines',
        name='Sell Threshold'
        ))
    
    return fig

# generate yield graph figure for given ticker 
# returns a graph_objects Figure object for use in dashboard

def generate_yield_graph(in_ticker, in_market, in_home_path):
    

    dfs = pd.read_csv(f'{in_home_path}datasets/yield_history/yield_history_{in_market}_{in_ticker}.csv')
    value_array = dfs['Daily Yield']
    date_array = dfs['Date']
 
    colors = {
        'background': '#111111',
        'text': '#7FDBFF'
        }
   
    peaks = find_peaks(value_array, prominence=0.004)[0]
    valleys = find_peaks(-value_array, prominence=0.004)[0]

    fig = go.Figure()
    #fig.layout.plot_bgcolor = colors['background']
    
    fig.add_trace(go.Scatter(
        x=date_array, 
        y=value_array,
        mode='lines+markers',
        name='Dividend Yield'
        ))

    fig.add_trace(go.Scatter(
        x=[date_array[i] for i in peaks],
        y=[value_array[j] for j in peaks],
        mode='markers',
        marker=dict(
            size=8,
            color='green',
            symbol='cross'
            ),
        name='Detected Peaks'
        ))

    fig.add_trace(go.Scatter(
        x=[date_array[i] for i in valleys],
        y=[value_array[j] for j in valleys],
        mode='markers',
        marker=dict(
            size=8,
            color='red',
            symbol='cross'
            ),
        name='Detected Valleys'
        ))

    total =0 
    for temp in peaks:
        total += value_array[temp] 
    
    peak_avg = total/len(peaks)
    print(f"Peak average value (total data set) {peak_avg}")

    total =0 
    for temp in valleys:
        total += value_array[temp] 
    
    valley_avg = total/len(valleys)
    print(f"Vally average value (total data set) {valley_avg}")

    peak_avg_list = [peak_avg]*len(dfs.index)
    valley_avg_list = [valley_avg]*len(dfs.index)

    fig.add_trace(go.Scatter(
        x=date_array, 
        y=peak_avg_list,
        mode='lines',
        name='Buy Threshold'
        ))
    
    
    fig.add_trace(go.Scatter(
        x=date_array, 
        y=valley_avg_list,
        mode='lines',
        name='Sell Threshold'
        ))
    
    return fig

def generate_price_graph(in_ticker, in_market, in_home_path):
    
    
    if in_market == 'tsx':
        in_ticker = in_ticker + '.TO'
    
    dfs = pd.read_csv(f'{in_home_path}datasets/price_history/yahoo_price_history_{in_ticker}.csv')
    value_array = dfs['Close']
    date_array = dfs['Date']
 
    colors = {
        'background': '#111111',
        'text': '#7FDBFF'
        }
   
    fig = go.Figure()
    fig.layout.plot_bgcolor = colors['background']
    
    fig.add_trace(go.Scatter(
        x=date_array,
        y=value_array,
        mode='lines+markers',
        name='Stock Price'
        ))
    
    return fig
    
   
def update_graph(in_market, in_tick):
    
    dfs5 = pd.read_csv(f'./datasets/yield_history/yield_history_{in_market}_{in_tick}.csv')

    value_array = dfs5['Daily Yield']
    date_array = dfs5['Date']
    peaks = find_peaks(value_array, prominence=0.001)[0]
    valleys = find_peaks(-value_array, prominence=0.001)[0]


    fig = go.Figure()
    fig.add_trace(go.Scatter(
        y=value_array,
        mode='lines+markers',
        name='Original Plot'
    ))

    fig.add_trace(go.Scatter(
        x=peaks,
        y=[value_array[j] for j in peaks],
        mode='markers',
        marker=dict(
            size=8,
            color='red',
            symbol='cross'
            ),
        name='Detected Peaks'
    ))

    fig.add_trace(go.Scatter(
        x=valleys,
        y=[value_array[j] for j in valleys],
        mode='markers',
        marker=dict(
            size=8,
            color='green',
            symbol='cross'
            ),
        name='Detected Valleys'
    ))

    print(f"Producing graph for {in_market} / {in_tick}")
    total =0 
    for temp in peaks:
        total += value_array[temp] 
    
    peak_avg = total/len(peaks)
    print(f"Peak average value (total data set) {peak_avg}")

    total =0 
    for temp in valleys:
        total += value_array[temp] 
    
    valley_avg = total/len(valleys)
    print(f"Vally average value (total data set) {valley_avg}")

    return fig