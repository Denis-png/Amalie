import dash
from dash.dependencies import Input, Output, State
import dash_table
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from django_plotly_dash import DjangoDash

from dashboard.models import *

app = DjangoDash('Table_Edit', external_stylesheets=[dbc.themes.BOOTSTRAP])

params = [
    'Weight', 'Torque', 'Width', 'Height',
    'Efficiency', 'Power', 'Displacement'
]


def get_fields():
    field_list = []
    for f in Sensors._meta.get_fields():
        if f.name == 'id' or f.name == 'calibrated_on':
            field_list.append({'name': f.name, 'id': f.name, 'editable': False})
        else:
            field_list.append({'name': f.name, 'id': f.name})
    return field_list


def get_field_values():
    data = []
    columns = get_fields()
    for row in Sensors.objects.using('global').values_list():
        count = 0
        temp_row = {}
        for col in columns:
            temp_row.update({col['id']: row[count]})
            count += 1
        data.append(temp_row)
    return data


app.layout = html.Div([
    html.Link(
            rel='stylesheet',
            href='/static/partitials/css/buttons.css'
        ),
    html.Link(
            rel='stylesheet',
            href='/static/partitials/css/labels.css'
        ),
    dcc.Location(id='url'),
    html.Div(id='output-container', className='custom-table d-flex justify-content-center'),
    html.Div(id='output-container-1'),
    html.Button('+', id='editing-rows-button', n_clicks=0, className='btn custom-button-static mt-3'),
    html.Button('Confirm changes', id='confirm-button', n_clicks=0, className='btn custom-button ml-2 mt-3')

])


@app.callback(
    Output('output-container', 'children'),
    Input('url', 'pathname'),
)
def update_table(pathname):
    return dash_table.DataTable(
        id='table-editing',
        columns=(get_fields()),
        data=get_field_values(),
        row_deletable=True,
        editable=True,
        style_cell={
            'color': '#2a5d68',
            'padding': '5px',
        },
    )


@app.callback(
    Output('table-editing', 'data'),
    Input('editing-rows-button', 'n_clicks'),
    State('table-editing', 'data'),
    State('table-editing', 'columns')
)
def add_row(n_clicks, rows, cols):
    if n_clicks > 0:
        rows.append({c['id']: '' for c in cols})
    return rows


@app.callback(
    Output('output-container-1', 'children'),
    Input('table-editing', 'data'),
    Input('confirm-button', 'n_clicks')
)
def save_changes(data, n):
    if n > 0:
        button_id = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
        if button_id == 'confirm-button':
            remove(data)
            create(data)
            update(data)
            return 'Updated'


'''
FUNCTIONS FOR THE DATA TABLE OPERATIONS
'''


# ADD ROW
def create(data):
    for row in data:
        try:
            Sensors.objects.using('global').get(id=row['id'])
        except ValueError:
            sensor = Sensors(sensor_id=row['sensor_id'], sensor_name=row['sensor_name'],
                             company=row['company'], measured_quantity=row['measured_quantity'],
                             geometry=row['geometry'],
                             calibration_interval=row['calibration_interval'], units=row['units'])
            sensor.save(using='global')
            return row['sensor_id']


# REMOVE ROW
def remove(data):
    db_list = Sensors.objects.using('global').values('id')
    new_list = [row['id'] for row in data]
    removed = []
    for sensor in db_list:
        if sensor['id'] not in new_list:
            removed.append(sensor['id'])
            Sensors.objects.using('global').get(id=sensor['id']).delete()
    return removed


# UPDATE
def update(data):
    for row in data:
        if row['id']:
            row_id = row.pop('id')
            Sensors.objects.filter(id=row_id).using('global').update(**row)
    return 'done'





