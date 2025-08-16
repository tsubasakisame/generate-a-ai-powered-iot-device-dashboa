import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import random

# IoT Device Data
device_data = {
    "device_id": [f"device_{i}" for i in range(10)],
    "temperature": [random.uniform(20, 30) for _ in range(10)],
    "humidity": [random.uniform(50, 70) for _ in range(10)],
    "pressure": [random.uniform(900, 1100) for _ in range(10)],
}

df = pd.DataFrame(device_data)

# Create a Dash app
app = dash.Dash(__name__)

# Define the layout
app.layout = html.Div(children=[
    html.H1(children='AI-Powered IoT Device Dashboard'),

    html.Div(children='''
        This dashboard displays real-time data from IoT devices.
    ''"),

    dcc.Dropdown(
        id='device-dropdown',
        options=[{'label': i, 'value': i} for i in df['device_id']],
        value=df['device_id'][0]
    ),

    dcc.Graph(id='live-update-graph'),

    dcc.Interval(
        id='interval-component',
        interval=1*1000, # in milliseconds
        n_intervals=0
    )
])

# Define the callback
@app.callback(
    Output('live-update-graph', 'figure'),
    [Input('interval-component', 'n_intervals'),
     Input('device-dropdown', 'value')]
)
def update_graph_live(n, device_id):
    filtered_df = df[df['device_id'] == device_id]
    fig = px.line(filtered_df, x=filtered_df.index, y='temperature')
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)