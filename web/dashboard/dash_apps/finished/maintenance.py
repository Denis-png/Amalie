import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash import dcc
from dash.dependencies import Output, Input
from django_plotly_dash import DjangoDash
from datetime import date
from dashboard.models import Maintenanceactions, Maintenance, People
from users.models import *

import datetime

app = DjangoDash('Maintenance_form', external_stylesheets=[dbc.themes.BOOTSTRAP])


def options():
    actions = Maintenanceactions.objects.all().using('global').values('label', 'value')
    return list(actions)


def user_options():
    options = []
    for user in People.objects.all().using('global').values('email', 'first_name', 'last_name'):
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
            initial_visible_month=datetime.datetime.now().date(),
            className='mb-1'
        ),
        dcc.RadioItems(id='selected_sensor', value=0),
        dcc.Input(id='time', placeholder='HH:MM:SS', className='mb-1', value='00:00:00'),
        dcc.Location(id='url'),
        html.Br(),
        dcc.Textarea(id='note', value='Type your note here...'),
        html.Div(id='output-container', style={'margin-top': '5px'}),
        html.Button('Confirm', id='confirm', type='submit', n_clicks=0, style={'margin-top': '5px'}, className='btn custom-button'),
        html.Div(id='output-container-text')
    ], className='flex'

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
    Output('output-container-text', 'children'),
    Input('my-date-picker-single1', 'date'),
    Input('time', 'value'),
    Input('actions', 'value'),
    Input('users', 'value'),
    Input('note', 'value'),
    Input('confirm', 'n_clicks')
)
def update_output(date_value, time_string, value, user1, note, n_clicks, request, **kwargs):
    if n_clicks > 0:
        button_id = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
        if date_value is not None and time_string is not None:
            date_object = date.fromisoformat(date_value)
            date_string = datetime.datetime.strptime(date_object.strftime('%Y-%m-%d'), '%Y-%m-%d')
            time_value = datetime.datetime.strptime(time_string, '%H:%M:%S')
            user_id = People.objects.using('global').get(email=user1).id
            sensor_id = request.session.get('selected_sensor')

            if button_id == 'confirm' and value is not None and user1 is not None:
                new = Maintenance(date=date_string, time=time_value, user_id=user_id, action=value, note=note, sensor_id=sensor_id)
                new.save(using='global')
                return 'DONE'



