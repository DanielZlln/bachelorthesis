from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
from data.clean_data import neutor_weekday

df_neutor_weekday = neutor_weekday()

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

# Data
df = px.data.iris()

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
                    drawFigure()
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