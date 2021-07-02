from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .decorators import *
from django.shortcuts import render, redirect
from django.views import View
from .forms import *
from .models import *

from users.models import CustomUser


# GENERAL BASE VIEW FOR THE DASHBOARD PAGE
class DashboardView(View):
    def __init__(self):
        pass

    @method_decorator(login_required)
    def get(self, req):
        if req.user.is_authenticated:
            return render(req, '../templates/dashboard/global.html', {})
        return redirect('login')

    @method_decorator(login_required)
    def post(self,req):
        pass


# INITIAL VIEW FOR SENSOR SELECTION
decorators = [login_required, tech_required]


class SensorsView(View):
    def __init__(self):
        self.sensor = SelectSensor()

    @method_decorator(decorators)
    def get(self,req):
        return render(req, '../templates/dashboard/sensors.html', {'select_sensor': self.sensor})

    @method_decorator(decorators)
    def post(self, req):
        sensor = SelectSensor(req.POST)
        if sensor.is_valid():
            cd = sensor.cleaned_data
            table = Sensors.objects.filter(sensor_id=cd['sensor_id']).using('global')
            req.session['selected_sensor'] = cd['sensor_id']
            return render(req, '../templates/dashboard/sensors.html', {'select_sensor': sensor, 'data': table})


# INITIAL VIEW FOR DATA QUALITY
class DataQView(View):
    def __init__(self):
        self.sensor = SelectSensor()
        self.table = Sensors.objects.all().using('global')

    def get(self,req):
        table = self.table
        return render(req, '../templates/dashboard/data_qual.html', {'data': table.values(), 'select_sensor': self.sensor})

    def post(self,req):
        pass


class HistoryView(View):
    def __init__(self):
        self.sensor = SelectSensor()
        self.table = Sensors.objects.all().using('global')

    def get(self,req):
        table = self.table
        return render(req, '../templates/dashboard/history.html', {'data': table.values(), 'select_sensor': self.sensor})

    def post(self,req):
        pass


# ADMIN VIEW
class AdminView(View):
    def __init__(self):
        self.action_form = AddAction()
        self.sensor_form = AddSensorForm()
        self.action_list = list(MaintenanceActions.objects.all().using('global').values_list('label', 'value'))
        self.sensor_list = list(Sensors.objects.all().using('global'))

    def get(self, req):
        return render(req, 'dashboard/admin.html', {'action_form': self.action_form, 'action_list': self.action_list, 'add_sensor': self.sensor_form, 'sensor_list': self.sensor_list})

    def post(self, req):
        if 'add_action' in req.POST:
            action_form = AddAction(req.POST)
            if action_form.is_valid():
                cd = action_form.cleaned_data
                action = MaintenanceActions(label=cd['action'], value=cd['action'])
                action.save(using='global')
                self.action_list = list(MaintenanceActions.objects.all().using('global').values_list('label', 'value'))
                return render(req, 'dashboard/admin.html', {'action_form': self.action_form, 'action_list': self.action_list, 'add_sensor': self.sensor_form, 'sensor_list': self.sensor_list})
        elif 'add_sensor' in req.POST:
            sensor_form = AddSensorForm(req.POST)
            if sensor_form.is_valid():
                cd = sensor_form.cleaned_data
                sensor = Sensors(sensor_id=cd['sensor_id'], sensor_name=cd['sensor_name'],
                                 company=cd['company'], measured_quantity=cd['measured_quantity'],
                                 calibration_interval=cd['calibration_interval'],
                                 units=cd['units'])
                sensor.save(using='global')
                self.sensor_list = list(Sensors.objects.all().using('global'))
                return render(req, 'dashboard/admin.html',
                              {'action_form': self.action_form, 'action_list': self.action_list, 'add_sensor': self.sensor_form, 'sensor_list': self.sensor_list})
        else:
            to_remove = req.POST['remove_action']
            print(to_remove)
            MaintenanceActions.objects.filter(label=to_remove).using('global').delete()
            self.action_list = list(MaintenanceActions.objects.all().using('global').values_list('label', 'value'))
            return render(req, 'dashboard/admin.html',
                              {'action_form': self.action_form, 'action_list': self.action_list, 'add_sensor': self.sensor_form, 'sensor_list': self.sensor_list})

        return render(req, 'dashboard/admin.html',
                          {'action_form': self.action_form, 'action_list': self.action_list, 'add_sensor': self.sensor_form, 'sensor_list': self.sensor_list})


