import json
import pandas as pd


from plotly.offline import plot
import plotly.graph_objects as go
import plotly.express as px
import dash_core_components as dcc
import dash_html_components as html
import dash

from django_plotly_dash import DjangoDash

app = DjangoDash('Plot', add_bootstrap_links=True)   # replaces dash.Dash

app.css.append_css({'external_url': '/static/partitials/css/tabs.css'})

app.layout = html.Div([
    dcc.Tabs(id='options', value='line', children=[
        dcc.Tab(
            label='Line',
            value='line',
            className='custom-tab',
            selected_className='custom-tab--selected'
        ),
        dcc.Tab(
            label='Histogram',
            value='hist'
        ),
        dcc.Tab(
            label='Boxplot',
            value='box'
        ),
    ]),
    html.Div(
        dcc.Graph(
            id='output'
        )
    )
])

@app.callback(
    dash.dependencies.Output('output', 'figure'),
    [dash.dependencies.Input('options', 'value')])
def plot(value, request, **kwargs):
    data = json.loads(request.session.get('data'))
    df = pd.DataFrame(data)
    df.insert(3, 'datetime', pd.to_datetime(df['date'] + ' ' + df['time']))
    if value == 'line':
        fig = px.line(df, x='datetime', y='value', color='sensor_name')
        return fig
    elif value == 'hist':
        fig = px.histogram(df, x='sensor_name', y='value')
        return fig
    elif value == 'box':
        fig = px.box(df, x='sensor_name', y='value')
        return fig




