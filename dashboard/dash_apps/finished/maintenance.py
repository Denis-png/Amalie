import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from dash.dependencies import Output, Input
from django_plotly_dash import DjangoDash
from datetime import date
from dashboard.models import MaintenanceActions
from users.models import *

app = DjangoDash('Maintenance_form', external_stylesheets=[dbc.themes.BOOTSTRAP])


def options():
    actions = MaintenanceActions.objects.all().using('global').values('label', 'value')
    return list(actions)


def user_options():
    options = []
    for user in CustomUser.objects.all().values('email', 'first_name', 'last_name'):
        name = user['first_name'] + ' ' + user['last_name']
        options.append({'label': name, 'value': user['email']})
    return options


app.layout = html.Div(
    [
        html.Link(
            rel='stylesheet',
            href='/static/partitials/css/buttons.css'
        ),
        dcc.DatePickerSingle(
            id='my-date-picker-single1',
            min_date_allowed=date(2021, 5, 20),
            initial_visible_month=date(2021, 5, 20),
        ),
        dcc.Location(id='url'),
        html.Div(id='output-container', style={'margin-top': '5px'}),
        html.Button('Confirm', id='confirm', type='submit', n_clicks=0, style={'margin-top': '5px'}, className='btn custom-button'),
    ],

)


@app.callback(
    Output('output-container', 'children'),
    Input('url', 'pathname'),
)
def update_input(pathname):
    return html.Div([
        dcc.Dropdown(
            id='actions',
            options=options(),
            value='Calibration',
            style={'margin-top': '5px'}
        ),
        dcc.Dropdown(
            id='users',
            options=user_options(),
            style={'margin-top': '5px'}
        ),
        html.Div(id='output-container-date-picker-single'),
    ])

@app.callback(
    Output('output-container-date-picker-single', 'children'),
    Input('my-date-picker-single1', 'date'),
    Input('actions', 'value'),
    Input('users', 'value'),
    Input('confirm', 'n_clicks')
)
def update_output(date_value, value, user, n_clicks):
    if n_clicks > 0:
        button_id = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
        if date_value is not None:
            date_object = date.fromisoformat(date_value)
            date_string = date_object.strftime('%B %d, %Y')
            if button_id == 'confirm' and value is not None and user is not None:
                string_prefix = '{} was perfomed on: '.format(value)
                return string_prefix + date_string + ' by ' + user



