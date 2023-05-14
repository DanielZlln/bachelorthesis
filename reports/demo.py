from data.clean_data import neutor_weekday
import plotly.graph_objects as go
import plotly.express as px
import dash
from dash import Dash, dcc, html, Input, Output

df_neutor_weekday = neutor_weekday()

app = Dash(__name__)

app.layout = html.Div([
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
])

@app.callback(
    Output('graph-with-slider', 'figure'),
    Input('yaxis-column', 'value'))
def update_figure(selected_column):
    fig = px.box(df_neutor_weekday, x='Wochentag', y=selected_column, points='all')
    fig.update_layout(transition_duration=500)
    return fig

if __name__ == '__main__':
    app.run_server(debug=False)

