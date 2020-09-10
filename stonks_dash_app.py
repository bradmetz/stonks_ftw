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
import plotly.graph_objects as go
from scipy.signal import find_peaks
from dash.dependencies import Input, Output
import numpy as np
import matplotlib.pyplot as plt


app = dash.Dash()



dfs5 = pd.read_csv('./datasets/yield_history/yield_history_nyse_T.csv')

value_array = dfs5['Daily Yield']
date_array = dfs5['Date']
peaks = find_peaks(value_array, prominence=0.004)[0]
valleys = find_peaks(-value_array, prominence=0.004)[0]


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

#fig.update_xaxes(date_array)

#fig.show()

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



colors = {
    'background': '#111111',
    'text': '#7FDBFF'
    }

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    
    html.H1(
        children='Stonks - Stock Recommendation Platform',
        style={
            'textAlign': 'center', 
            'color': colors['text']
            }
        ),
    html.Div(
        children='Dividend Yield Based Stock Picks', 
        style={
            'textAlign': 'center',
            'color':colors['text']
            }),
    
    html.Label('Choose your Exchange', style={'color':colors['text']}),
    dcc.RadioItems(
        id='in_market',
        options=[
            {'label': 'TSX', 'value': 'tsx'},
            {'label': 'NYSE', 'value':'nyse'},
            {'label': 'NASDAQ', 'value': 'nasdaq'}
            ],
        value='tsx',
        style={'color':colors['text']}
        ),
    html.Label('Enter your ticker', style={'color':colors['text']}),
    dcc.Input(
        id='in_tick',
        value='T',
        type = 'text'
        ),
    dcc.Graph(
        id='yield_graph',
        figure=fig
        ),         

 '''    
    dcc.Graph(
        id='Graph1',
        figure={
            'data': [
                {'x': [1,2,3], 'y': [4,1,2], 'type': 'bar', 'name': 'SF'},
                {'x': [1,2,3], 'y': [2,4,5], 'type': 'bar', 'name': 'Montreal'},
                ],
            'layout': {
                'plot_bgcolor':colors['background'],
                'paper_bgcolor': colors['background'],
                'font': {
                    'color':colors['text']
                    }
                }
            }
        ),  
   ''' 
   
    ]
)    
    
@app.callback(
    Output(component_id='yield_graph', component_property='figure'),
    [Input(component_id='in_market', component_property='value'),
     Input(component_id='in_tick', component_property='value')]
    )
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

#fig.update_xaxes(date_array)

    #fig.show()
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


if __name__ == '__main__':
    app.run_server(debug=True)
