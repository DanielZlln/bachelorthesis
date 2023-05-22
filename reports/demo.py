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

app = Dash(__name__)

app.layout = html.Div(children=[
    html.Div([
        dcc.Graph(id='graph-with-slider'),
        html.Div([
            dcc.Dropdown(
                options=[
                    {'label': 'Neutor', 'value': 'Neutor'},
                    {'label': 'Neutor EW', 'value': 'Neutor FR stadteinwärts'},
                    {'label': 'Neutor AW', 'value': 'Neutor FR stadtauswärts'}
                ],
                value='Neutor',
                id='yaxis-column'
            )
        ])
    ]),
    html.Div([ 
        dcc.Graph(id='tip-graph'),
        dcc.Graph(id='second-graph'),  # Neuer Graph
        ]),
    ])

@app.callback(
    Output('graph-with-slider', 'figure'),
    Input('yaxis-column', 'value'))
def update_figure(selected_column):
    fig = px.box(df_neutor_weekday, x='Wochentag', y=selected_column, points='all')
    #fig.update_layout(transition_duration=500)
    return fig

def update_second_figure():
    fig = px.box(df_neutor_last_week, x='Datum', y=['Neutor FR stadteinwärts', 'Neutor FR stadtauswärts'], points='all')
    return fig

if __name__ == '__main__':
    app.run_server(debug=False)

