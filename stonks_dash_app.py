# -*- coding: utf-8 -*-
"""
stonks_dash_app.py

Description:  Base script for Stonks web based dashboard.  This will be the 
main script for all visualizations and widgets for tuning. 

"""

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
from scipy.signal import find_peaks
from dash.dependencies import Input, Output
import numpy as np
import stonks_visualize as sv



app = dash.Dash(external_stylesheets=[dbc.themes.SLATE])


def draw_yield_graph():
    return  html.Div([
        dbc.Card(
            dbc.CardBody([
                dcc.Graph(
                    figure=sv.generate_yield_graph('T', 'tsx', './').update_layout(
                        template='plotly_dark',
                        plot_bgcolor= 'rgba(0, 0, 0, 0)',
                        paper_bgcolor= 'rgba(0, 0, 0, 0)',
                    ),
                    config={
                        'displayModeBar': False
                    }
                ) 
            ])
        ),  
    ])

def draw_price_graph():
    return  html.Div([
        dbc.Card(
            dbc.CardBody([
                dcc.Graph(
                    figure=sv.generate_price_graph('T', 'tsx', './').update_layout(
                        template='plotly_dark',
                        plot_bgcolor= 'rgba(0, 0, 0, 0)',
                        paper_bgcolor= 'rgba(0, 0, 0, 0)',
                    ),
                    config={
                        'displayModeBar': False
                    }
                ) 
            ])
        ),  
    ])

# Text field
def drawText():
    return html.Div([
        dbc.Card(
            dbc.CardBody([
                html.Div([
                    html.H2("Text"),
                ], style={'textAlign': 'center'}) 
            ])
        ),
    ])

app.layout = html.Div([
    html.H1(
        children='Stonks - Stock Recommendation Platform',
        style={
            'textAlign': 'center', 
            }
        ),
    dbc.Row([dbc.Col([html.Label('Choose your Exchange')]),
             
             dbc.Col([dcc.RadioItems(
                 id='in_market',
                 options=[
                     {'label': 'TSX', 'value': 'tsx'},
                {'label': 'NYSE', 'value':'nyse'},
                {'label': 'NASDAQ', 'value': 'nasdaq'}
                ],
                value='tsx',
                )]),
             dbc.Col([html.Label('Enter your ticker')]),
             dbc.Col([dcc.Input(
                 id='in_tick',
                 value='T',
                 type = 'text'
                 )]),
             ]),
    dbc.Card(
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    sv.generate_ticker_card('T', 'tsx')
                ], width=3),
                dbc.Col([
                    sv.generate_ticker_card('T', 'nyse')
                ], width=3),
                dbc.Col([
                    sv.generate_ticker_card('AAPL', 'nasdaq')
                ], width=3),
                dbc.Col([
                    sv.generate_ticker_card('ATD.B', 'tsx')
                ], width=3),
            ], align='center'), 
            html.Br(),
            dbc.Row([
                dbc.Col([
                    draw_yield_graph() 
                ], width=3),
                dbc.Col([
                    draw_price_graph()
                ], width=3),
                dbc.Col([
                    draw_yield_graph() 
                ], width=6),
            ], align='center'), 
            html.Br(),
            dbc.Row([
                dbc.Col([
                    draw_yield_graph()
                ], width=9),
                dbc.Col([
                    draw_yield_graph()
                ], width=3),
            ], align='center'),      
        ]), color = 'dark'
    )
])

# Run app and display result inline in the notebook
# app.run_server(mode='external')

if __name__ == '__main__':
    app.run_server(debug=True)
