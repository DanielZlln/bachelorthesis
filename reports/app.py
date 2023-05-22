import os
import sys
sys.path.append(os.path.dirname(os.getcwd()))
from data.clean_data import neutor_weekday, neutor_last_week
import plotly.graph_objects as go
import plotly.express as px
import dash
from dash import Dash, dcc, html, Input, Output

df_neutor_weekday = neutor_weekday()
df_neutor_last_week = neutor_last_week()

app = dash.Dash(__name__)

# CSS-Datei einbinden
app.css.append_css({
    'external_url': 'style.css'
})

app.layout = html.Div(
    children=[
        # Erste Reihe
        html.Div(
            className='first-row',  
            children=[
                html.Div(className='box small'),
                html.Div(className='box small'),
                html.Div(className='box small')
            ]
        ),

        # Zweite Reihe
        html.Div(
            className='second-row',  
            children=[
                html.Div(className='box mid'),
                html.Div(className='box big')
                        ]
        ),
        
        # Dritte Reihe
        html.Div(
            className='third-row',
            children=[
                html.Div(className='box mid'),
                html.Div(className='box big')
            ]
        )
    ]
)

if __name__ == '__main__':
    app.run_server(debug=False, port = 8051)
