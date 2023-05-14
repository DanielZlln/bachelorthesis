import plotly.graph_objects as go
import plotly.express as px

import dash
from dash import html, dcc
import dash_daq as daq
from dash.dependencies import Input, Output, State
# Graphs
histogram = px.histogram(test, x='Probability', color=TARGET, 
                         marginal="box", nbins=30)
barplot = px.bar(test.groupby('Binned probability', 
                              as_index=False)['Target'].mean(), 
                 x='Binned probability', y='Target')
columns = ['Age', 'Gender', 'Class', 'Embark town', TARGET, 
           'Probability']
table = go.Figure(data=[go.Table(
    header=dict(values=columns),
    cells=dict(values=[test[c] for c in columns])
)])
# ********************* Dash app *********************
app = dash.Dash(__name__)
app.layout = html.Div([
    html.Div([
        html.H1("Titanic predictions"),
        html.P("Summary of predicted probabilities for Titanic test dataset."),
        html.Img(src="assets/left_pane.png"),
        html.Label("Passenger class"), 
        dcc.Dropdown(multi=True,
                     options=create_dropdown_options(
                         test['Class']
                     ),
                     value=create_dropdown_value(
                         test['Class']
                     )),
        html.Label("Gender", className='dropdown-labels'), 
        dcc.Dropdown(multi=True,
                     options=create_dropdown_options(
                         test['Gender']
                     ),
                     value=create_dropdown_value(
                         test['Gender']
                     )),
        html.Button("Update"),
        ]),
    html.Div([
        html.Div([
            dcc.Graph(figure=histogram),
            dcc.Graph(figure=barplot)
        ]),
        html.Div([
            dcc.Graph(figure=table),
            html.Div([
                html.Label("Survival status"), 
                daq.BooleanSwitch(on=True),
                html.Label("Sort probability in an ascending order"),
                daq.BooleanSwitch(on=True),
                html.Label("Number of records"), 
                dcc.Slider(min=5, max=20, step=1, value=10, 
                           marks=create_slider_marks([5, 10, 
                                                      15, 20])),
            ]),
        ])
    ])
])
if __name__ == '__main__':
    app.run_server(debug=False)