import json

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from django.shortcuts import render
from django_plotly_dash import DjangoDash

app = DjangoDash('Sensors_Dashboard', external_stylesheets=[dbc.themes.BOOTSTRAP])

sidebar = html.Div(
    [
        html.H2("Dashboard"),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("Sensors", href="/sensors", active="exact"),
                dbc.NavLink("Data", href="/data", active="exact"),
                dbc.NavLink("History", href="/history", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
)

content = html.Div(id="page-content")

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname, request):
    if pathname == "/sensors":
        return html.P("Oh cool, this is page 2!")
    elif pathname == "/page-1":
        return html.P("Oh cool, this is page 2!")
    elif pathname == "/page-2":
        return html.P("Oh cool, this is page 2!")


