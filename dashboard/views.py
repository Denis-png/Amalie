import json

from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render
from django.views import View
from .forms import *
from .models import *


class DashboardView(View):
    def __init__(self):
        pass

    def get(self, req):
        return render(req, '../templates/dashboard/global.html', {})

    def post(self,req):
        pass


class SensorsView(View):
    def __init__(self):
        self.sensor = SelectSensor()

    def get(self,req):
        return render(req, '../templates/dashboard/sensors.html', {'select_sensor': self.sensor})

    def post(self, req):
        calibration_form = CalibrationDate()
        sensor = SelectSensor(req.POST)
        if sensor.is_valid():
            cd = sensor.cleaned_data
            table = Sensors.objects.filter(sensor_id=cd['sensor_id']).using('global')
            return render(req, '../templates/dashboard/sensors.html', {'select_sensor': sensor, 'calibration': calibration_form, 'data': table})


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
