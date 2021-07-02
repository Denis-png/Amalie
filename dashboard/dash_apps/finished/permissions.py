import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from users.models import *
from dash.dependencies import Output, Input
from django_plotly_dash import DjangoDash


app = DjangoDash('Permissions_form', external_stylesheets=[dbc.themes.BOOTSTRAP])


app.layout = html.Div(
    [
        html.Link(
            rel='stylesheet',
            href='/static/partitials/css/buttons.css'
        ),
        dcc.Location(id='url'),
        html.Div(id='output-container'),
        dcc.Dropdown(
            id='permission',
            options=[
                {'label': 'Common', 'value': 'common'},
                {'label': 'Technician', 'value': 'tech'},
                {'label': 'Scientist', 'value': 'sci'},
            ],
            className='form-select form-select-sm mt-2'
        ),
        html.Button('Update', id='upgrade', type='submit', n_clicks=0, className='btn custom-button mt-3'),
        html.Div(id='output-container-users'),
    ],
)


@app.callback(
    Output('output-container', 'children'),
    Input('url', 'pathname'),
)
def update_input(pathname):
    return html.Div(
        dcc.Dropdown(
            id='users',
            options=[{'label': user['first_name'] + ' ' + user['last_name'] + ' ({})'.format(user['email']), 'value': user['email']} for user in
                     CustomUser.objects.all().values('email', 'first_name', 'last_name')]
        )
    )


@app.callback(
    Output('output-container-users', 'children'),
    Input('users', 'value'),
    Input('permission', 'value'),
    Input('upgrade', 'n_clicks')
)
def update_output(email, role, n_clicks):
    string_prefix = 'You have updated user '
    if email is not None:
        if n_clicks > 0:
            button_id = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
            if button_id == 'upgrade':
                if role == 'common':
                    CustomUser.objects.filter(email=email).update(is_technician=False, is_scientist=False)
                elif role == 'tech':
                    CustomUser.objects.filter(email=email).update(is_technician=True)
                elif role == 'sci':
                    CustomUser.objects.filter(email=email).update(is_scientist=True)
                return string_prefix + email + ' with role ' + role



