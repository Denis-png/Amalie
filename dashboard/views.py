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

    def get(self, req):
        return render(req, 'dashboard/admin.html', {'aciton_form': self.action_form})

    def post(self, req):
        action_form = AddAction(req.POST)
        if action_form.is_valid():
            cd = action_form.cleaned_data
            action = MaintenanceActions(label=cd['action'], value=cd['action'])
            action.save(using='global')
            return render(req, 'dashboard/admin.html', {'aciton_form': self.action_form})


