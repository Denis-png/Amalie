import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from dashboard.models import *
from dash.dependencies import Output, Input
from django_plotly_dash import DjangoDash
from datetime import date

app = DjangoDash('Calibration_form', external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div(
    [
        html.Link(
            rel='stylesheet',
            href='/static/partitials/css/buttons.css'
        ),
        dcc.DatePickerSingle(
            id='my-date-picker-single',
            min_date_allowed=date(2021, 5, 20),
            initial_visible_month=date(2021, 5, 20),
        ),
        html.Button('Update', id='update', type='submit', n_clicks=0, className='btn custom-button ml-3'),
        html.Div(id='output-container-date-picker-single'),
    ],
)


@app.callback(
    Output('output-container-date-picker-single', 'children'),
    Input('my-date-picker-single', 'date'),
    Input('update', 'n_clicks')
)
def update_output(date_value, n_clicks, request):
    string_prefix = 'You have updated calibration date with: '
    if date_value is not None:
        date_object = date.fromisoformat(date_value)
        date_string = date_object.strftime('%B %d, %Y')
        if n_clicks > 0:
            sensor_id = request.session.get('selected_sensor')
            Sensors.objects.filter(sensor_id=sensor_id).using('global').update(calibrated_on=date_object)
            return string_prefix + date_string



