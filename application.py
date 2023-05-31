import os
import sys
sys.path.append(os.path.dirname(os.getcwd()))
from data.clean_data_dash import neutor_weekday, neutor_last_week, load_data
import plotly.graph_objects as go
import plotly.express as px
import dash
from dash import Dash, dcc, html, Input, Output
import pandas as pd

df_neutor = load_data()
df_neutor_weekday = neutor_weekday()
df_neutor_last_week = neutor_last_week()

max_time = df_neutor.groupby('Zeit')['Neutor'].mean().idxmax()
formatted_time = max_time.strftime("%H:%M")

app = dash.Dash(__name__)
application = app.server 

app.layout = html.Div(
        children=[
        html.Div(
            className='first-row',
            children=[
                html.Img(
                    src=r'assets/logo-sw-rahmen.jpg',
                    alt='image',
                    style={
                        "height": "60px",
                        "width": "auto"
                    }
                )
            ]
        ),
        # Erste Reihe
        html.Div(
            className='first-row',
            children=[
                html.Div(
                    className='box small',
                    children=[
                        html.H6(children='Max. Verkehr Tag',
                                style={
                                    'textAlign': 'center',
                                    'color': 'white',
                                    'margin-top': '10px',
                                    'fontSize': 18
                                }),
                        html.P(df_neutor.groupby('Datum')['Neutor'].sum().max(),
                                style={
                                    'textAlign': 'center',
                                    'color': 'white',
                                    'fontSize': 30,
                                    'margin-top': '-40px'
                                }),
                        html.P(f"Datum: {df_neutor.groupby('Datum')['Neutor'].sum().idxmax()}",
                                style={
                                    'textAlign': 'center',
                                    'color': 'white',
                                    'fontSize': 12,
                                    'margin-top': '-25px'
                                })
                    ]
                ),
                html.Div(
                    className='box small',
                    children=[
                        html.H6(children='Min. Verkehr Tag',
                                style={
                                    'textAlign': 'center',
                                    'color': 'white',
                                    'margin-top': '10px',
                                    'fontSize': 18
                                }),
                        html.P(df_neutor.groupby('Datum')['Neutor'].sum().min(),
                                style={
                                    'textAlign': 'center',
                                    'color': 'white',
                                    'fontSize': 30,
                                    'margin-top': '-40px'
                                }),
                        html.P(f"Datum: {df_neutor.groupby('Datum')['Neutor'].sum().idxmin()}",
                                style={
                                    'textAlign': 'center',
                                    'color': 'white',
                                    'fontSize': 12,
                                    'margin-top': '-25px'
                                })
                    ]
                ),
                html.Div(
                    className='box small',
                    children=[
                        html.H6(children='Höchster Verkehr pro Stunde',
                                style={
                                    'textAlign': 'center',
                                    'color': 'white',
                                    'margin-top': '10px',
                                    'fontSize': 18
                                }),
                        html.P(df_neutor.groupby('Zeit')['Neutor'].mean().max().round(),
                                style={
                                    'textAlign': 'center',
                                    'color': 'white',
                                    'fontSize': 30,
                                    'margin-top': '-40px'
                                }),
                        html.P(f"Uhrzeit: {formatted_time}",
                                style={
                                    'textAlign': 'center',
                                    'color': 'white',
                                    'fontSize': 12,
                                    'margin-top': '-25px'
                                })
                    ]
                )
            ]
        ),

        # Zweite Reihe
        html.Div(
            className='second-row',  
            children=[
                html.Div(className='box mid',
                         children=[
                             html.Div('Platzhalter')],
                         style={'color': 'white'}),
                html.Div(className='box big',
                         style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center'},
                         children=[
                             dcc.Graph(
                                 figure=go.Figure(
                                     data=[
                                         go.Bar(
                                             name='SEin',
                                             x=df_neutor_last_week['Datum'],
                                             y=df_neutor_last_week['Neutor FR stadteinwärts'],
                                             offsetgroup=0
                                         ),
                                         go.Bar(
                                             name='SAus',
                                             x=df_neutor_last_week['Datum'],
                                             y=df_neutor_last_week['Neutor FR stadtauswärts'],
                                             offsetgroup=0,
                                             base=df_neutor_last_week['Neutor FR stadteinwärts']
                                         )
                                     ],
                                     layout=go.Layout(
                                         title={
                                             'text': 'Verkehr der letzten 7 Tage',
                                             'y': 0.9,
                                             'x': 0.5,
                                             'xanchor': 'center',
                                             'yanchor': 'top'},
                                         showlegend=True,
                                         xaxis=dict(title='Datum'),
                                         yaxis=dict(title='Anzahl'),
                                         plot_bgcolor='rgba(0,0,0,0)',
                                         template='plotly_dark',
                                         paper_bgcolor='rgba(0,0,0,0)'
                                        )
                                    )
                                )
                            ])
                        ]
        ),
        
        # Dritte Reihe
        html.Div(
            className='third-row',
            children=[
                html.Div(className='box mid',
                        children=[
                            html.Div('Platzhalter')],
                         style={'color': 'white'}),
                html.Div(
                    className='box big',
                    style={'display': 'flex', 'flex-direction': 'column', 'align-items': 'center'},
                    children=[
                        html.Div(
                            dcc.Dropdown(
                                options=[
                                    {'label': 'Neutor','value': 'Neutor'},
                                    {'label': 'Neutor EW', 'value': 'Neutor FR stadteinwärts'},
                                    {'label': 'Neutor AW', 'value': 'Neutor FR stadtauswärts'}
                                ],
                                value='Neutor',
                                id='yaxis-column',
                                style={'backgroundColor': 'rgb(24, 21, 21)', 'color': 'MediumTurqoise'}
                            ),
                            style={'align-self': 'center',
                                   'width': '40%'}
                        ),
                        dcc.Graph(id='boxplot_wd')
                    ]
                )
            ]
        )
    ]
)


@app.callback(
    Output('boxplot_wd', 'figure'),
    Input('yaxis-column', 'value'))
def update_figure(selected_column):
    fig = px.box(df_neutor_weekday, x='Wochentag', y=selected_column, points='all')
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        title="Boxplot für die Visualisierung des Verkehrs an den einzelnen Wochentagen",
    )
    return fig

if __name__ == '__main__':
    application.run(debug=True)
