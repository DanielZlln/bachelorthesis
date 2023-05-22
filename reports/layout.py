from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
import os
import sys
sys.path.append(os.path.dirname(os.getcwd()))
from data.clean_data import neutor_weekday, neutor_last_week

df_neutor_weekday = neutor_weekday()
df_neutor_last_week = neutor_last_week()

# Iris bar figure
def drawFigure():
    return  html.Div([
        dbc.Card(
            dbc.CardBody([
                dcc.Graph(
                    fig = px.box(df_neutor_weekday, x='Wochentag', y='Neutor', points='all'
                    ).update_layout(
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
    
def drawFigure_sec():
    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            name='SE',
            x=df_neutor_last_week['Datum'],
            y=df_neutor_last_week['Neutor FR stadteinwärts'],
            offsetgroup=0
        )
    )
    fig.add_trace(
        go.Bar(
            name='SA',
            x=df_neutor_last_week['Datum'],
            y=df_neutor_last_week['Neutor FR stadtauswärts'],
            offsetgroup=0,
            base=df_neutor_last_week['Neutor FR stadteinwärts']
        )
    )
    
    return html.Div([
        dbc.Card(
            dbc.CardBody([
                dcc.Graph(
                    figure=fig.update_layout(
                        template='plotly_dark',
                        plot_bgcolor='rgba(0, 0, 0, 0)',
                        paper_bgcolor='rgba(0, 0, 0, 0)',
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

# Build App
app = Dash(external_stylesheets=[dbc.themes.SLATE])

app.layout = html.Div([
    dbc.Card(
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    drawText()
                ], width=3),
                dbc.Col([
                    drawText()
                ], width=3),
                dbc.Col([
                    drawText()
                ], width=3),
            ], align='center'), 
            html.Br(),
            dbc.Row([
                dbc.Col([
                    drawFigure() 
                ], width=3),
                dbc.Col([
                    drawFigure()
                ], width=3),
                dbc.Col([
                    drawFigure() 
                ], width=6),
            ], align='center'), 
            html.Br(),
            dbc.Row([
                dbc.Col([
                    drawFigure_sec()
                ], width=7),
                dbc.Col([
                    drawFigure()
                ], width=3),
            ], align='center'),      
        ]), color = 'dark'
    )
])

# Run app and display result inline in the notebook
app.run_server()