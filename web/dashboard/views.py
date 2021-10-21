import json
import csv
from datetime import datetime, date

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from .decorators import *
from django.apps import apps
from django.shortcuts import render, redirect
from django.views import View
from .forms import *
from .models import *
from users.models import CustomUser


# DASHBOARD HOME VIEW
class DashboardView(View):
    def __init__(self):
        self.ctx = {}

    def get(self, req):
        if req.user.is_authenticated:
            return render(req, '../templates/dashboard/global.html', {})
        return redirect('login')

    @method_decorator(login_required)
    def post(self, req):
        pass


decorators = [login_required, tech_required]


# QUERY VIEWs
class QueryView(View):
    def __init__(self):
        self.data_variables = [x for x in apps.get_app_config('dashboard').get_models() if 'data_' in x.__name__]
        self.var_names = [x.__name__.split('_')[1] for x in apps.get_app_config('dashboard').get_models() if
                          'data_' in x.__name__]
        self.ctx = {}

    @method_decorator(decorators)
    def get(self, req):
        self.ctx['var_names'] = self.var_names
        return render(req, '../templates/dashboard/query/query.html', self.ctx)

    @method_decorator(decorators)
    def post(self, req):
        self.ctx['var_names'] = self.var_names
        self.ctx['date_range'] = req.POST.get('datepicker')
        date_range = []
        for date in req.POST.get('datepicker').split(' - '):
            date_range.append(date)
        for var in self.data_variables:
            if req.POST.get('var_names') == var.__name__.split('_')[1]:
                self.ctx['selected'] = var.__name__.split('_')[1]
                to_plot = {'x': [], 'y': []}
                try:
                    data = var.objects.filter(date__gt=date_range[0], date__lt=date_range[1]).using('global')
                except:
                    data = var.objects.all().using('global')

                req.session['data'] = json.dumps(list(data.values()), cls=DjangoJSONEncoder)
                self.ctx['table'] = var.__name__.split('_')[1]
                self.ctx['data'] = data

        return render(req, '../templates/dashboard/query/query.html', self.ctx)


@login_required
def save_data(req):
    if req.method == 'POST':
        save_format = req.POST.get('save_format')
        if save_format == 'csv':
            data = json.loads(req.session.get('data'))
            res = HttpResponse(content_type='text/csv')
            res['Content-Disposition'] = 'attachment; filename="data.csv"'
            writer = csv.writer(res)
            writer.writerow(['id', 'sensor_name', 'date', 'time', 'value', 'signal'])
            for row in data:
                writer.writerow(row.values())
        elif save_format == 'json':
            data = json.loads(req.session.get('data'))
            save_dt = json.dumps(data)
            res = HttpResponse(save_dt, content_type='application/json')
            res['Content-Disposition'] = 'attachment; filename="data.json"'
    return res


# MAINTENANCE VIEW
class MaintenanceView(View):
    def __init__(self):
        self.ctx = dict()
        self.ctx['sensors'] = Sensors.objects.all().using('global').values('id', 'sensor_name')
        actions = Maintenanceactions.objects.all().using('global').values('label', 'value')
        self.ctx['actions'] = list(actions)

    def get(self, req):
        return render(req, '../templates/dashboard/maintenance/maintenance.html', self.ctx)

    def post(self, req):
        req.session['sensor'] = json.dumps(req.POST.get('sensor'), cls=DjangoJSONEncoder)

        return render(req, '../templates/dashboard/maintenance/maintenance.html', self.ctx)


def maintenance(req):
    print(req.POST)
    user = req.user
    user_id = People.objects.using('global').get(email=user).id
    date = req.POST.get('date_time').split(' ')[0]
    time = req.POST.get('date_time').split(' ')[1]

    action = req.POST.get('actions')
    note = req.POST.get('note')
    sensor_id = json.loads(req.session.get('sensor'))

    new = Maintenance(date=date, time=time, user_id=user_id, action=action, note=note, sensor_id=sensor_id)
    new.save(using='global')

    return redirect('/maintenance/')


def update_actions(req):
    print(req.POST)
    if req.POST.get('to_remove'):
        to_remove = req.POST.get('to_remove')
        Maintenanceactions.objects.filter(label=to_remove).using('global').delete()
    if req.POST.get('to_add'):
        label_value = req.POST.get('to_add')
        new_action = Maintenanceactions(label=label_value, value=label_value)
        new_action.save(using='global')
    return redirect('/maintenance/')


def condition(req):
    print(req.POST)
    start_date = req.POST.get('start_date_time').split(' ')[0]
    start_time = req.POST.get('end_date_time').split(' ')[1]
    end_date = req.POST.get('start_date_time').split(' ')[0]
    end_time = req.POST.get('end_date_time').split(' ')[1]
    condition = req.POST.get('condition')
    note = req.POST.get('note')
    sensor_id = json.loads(req.session.get('sensor'))

    new = Condition(start_date=start_date, start_time=start_time, end_date=end_date, end_time=end_time, condition=condition, note=note, sensor_id=sensor_id)
    new.save(using='global')

    return redirect('/maintenance/')

# USERS VIEW
class UsersView(View):
    def __init__(self):
        self.ctx = {}
        self.sensor = SelectSensor()
        self.table = Sensors.objects.all().using('global')

    def get(self, req):
        table = self.table
        return render(req, '../templates/dashboard/history.html',
                      {'data': table.values(), 'select_sensor': self.sensor})

    def post(self, req):
        pass


# MAPS VIEW
class MapsView(View):
    def __init__(self):
        self.ctx = {}
        self.sensor = SelectSensor()
        self.table = Sensors.objects.all().using('global')

    def get(self, req):
        table = self.table
        return render(req, '../templates/dashboard/history.html',
                      {'data': table.values(), 'select_sensor': self.sensor})

    def post(self, req):
        pass


# ADMIN VIEW
class AdminView(View):
    def __init__(self):
        self.ctx = {}
        self.action_form = AddAction()
        self.person_form = AddPerson()
        self.action_list = list(Maintenanceactions.objects.all().using('global').values_list('label', 'value'))
        self.sensor_list = list(Sensors.objects.all().using('global'))

    def get(self, req):
        return render(req, 'dashboard/admin.html', {'action_form': self.action_form, 'action_list': self.action_list,
                                                    'sensor_list': self.sensor_list, 'person_form': self.person_form})

    def post(self, req):
        if 'add_action' in req.POST:
            action_form = AddAction(req.POST)
            if action_form.is_valid():
                cd = action_form.cleaned_data
                action = Maintenanceactions(label=cd['action'], value=cd['action'])
                action.save(using='global')
                self.action_list = list(Maintenanceactions.objects.all().using('global').values_list('label', 'value'))
                return render(req, 'dashboard/admin.html',
                              {'action_form': self.action_form, 'action_list': self.action_list,
                               'sensor_list': self.sensor_list})
        elif 'remove_action' in req.POST:
            to_remove = req.POST['remove_action']
            print(to_remove)
            Maintenanceactions.objects.filter(label=to_remove).using('global').delete()
            self.action_list = list(Maintenanceactions.objects.all().using('global').values_list('label', 'value'))
            return render(req, 'dashboard/admin.html',
                          {'action_form': self.action_form, 'action_list': self.action_list,
                           'sensor_list': self.sensor_list})
        elif 'add_person' in req.POST:
            person_form = AddPerson(req.POST)
            if person_form.is_valid():
                cd = person_form.cleaned_data
                person = People(first_name=cd['first_name'], last_name=cd['last_name'], email=cd['email'],
                                technician_czu=cd['technician_czu'], technician_company=cd['technician_company'],
                                sensor_type_id=int(cd['sensor_type'][0]))
                person.save(using='global')
                return render(req, 'dashboard/admin.html',
                              {'action_form': self.action_form, 'action_list': self.action_list,
                               'sensor_list': self.sensor_list, 'person_form': self.person_form})

        return render(req, 'dashboard/admin.html',
                      {'action_form': self.action_form, 'action_list': self.action_list,
                       'sensor_list': self.sensor_list, 'person_form': self.person_form})
