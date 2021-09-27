import dash
from dash.dependencies import Input, Output, State
import dash_table
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from django_plotly_dash import DjangoDash

from dashboard.models import *

models_list = [Sensors, SensorType, SensorVariable, SensorsGroup, API, Variables, Project]
models_options = []
for model in models_list:
    models_options.append({'label': model.__name__, 'value': model.__name__})

app = DjangoDash('Table_Edit', external_stylesheets=[dbc.themes.BOOTSTRAP])


def get_fields(model):
    field_list = []
    for f in model._meta.concrete_fields:
        if f.name == 'id':
            field_list.append({'name': f.name, 'id': f.name, 'editable': False})
        else:
            field_list.append({'name': f.name, 'id': f.name})
    return field_list


def get_field_values(model):
    data = []
    columns = get_fields(model)
    for row in model.objects.using('global').values_list():
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
    dcc.Dropdown(
        id='models_list',
        options=models_options,
        className='mb-3'

    ),
    dcc.Location(id='url'),
    html.Div(id='output-container', className='d-flex justify-content-center', style={"overflow-x": "scroll"}),
    html.Div(id='output-container-1'),
    html.Button('+', id='editing-rows-button', n_clicks=0, className='btn custom-button-static mt-3'),
    html.Button('Confirm changes', id='confirm-button', n_clicks=0, className='btn custom-button ml-2 mt-3')

])


@app.callback(
    Output('output-container', 'children'),
    Input('url', 'pathname'),
    Input('models_list', 'value'),
)
def update_table(pathname, model):
    for table in models_list:
        if model == table.__name__:
            return dash_table.DataTable(
                id='table-editing',
                columns=(get_fields(table)),
                data=get_field_values(table),
                row_deletable=True,
                editable=True,
                style_data={
                    'color': '#2a5d68',
                    'overflow': 'hidden',
                    'textOverflow': 'ellipsis',
                    'maxWidth': 0,
                    'whiteSpace': 'normal'
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
    Input('confirm-button', 'n_clicks'),
    Input('models_list', 'value'),
)
def save_changes(data, n, model):
    if n > 0:
        button_id = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
        if button_id == 'confirm-button':
            for table in models_list:
                if model == table.__name__:
                    remove(data, table)
                    create(data, table)
                    update(data, table)
                    return 'Updated'


'''
FUNCTIONS FOR THE DATA TABLE OPERATIONS
'''


# ADD ROW
def create(data, table):
    for row in data:
        try:
            table.objects.using('global').get(id=row['id'])
        except ValueError:
            new_row = {}
            for field, value in row.items():
                if value != '':
                    new_row.update({field: value})
            table.objects.using('global').create(**new_row)
            table.save(using='global')
    return table.__name__


# REMOVE ROW
def remove(data, table):
    db_list = table.objects.using('global').values('id')
    new_list = [row['id'] for row in data]
    removed = []
    for record in db_list:
        if record['id'] not in new_list:
            removed.append(record['id'])
            table.objects.using('global').get(id=record['id']).delete()

    return removed


# UPDATE
def update(data, table):
    for row in data:
        if row['id']:
            row_id = row.pop('id')
            table.objects.filter(id=row_id).using('global').update(**row)
    return 'done'





