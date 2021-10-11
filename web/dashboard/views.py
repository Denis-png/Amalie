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
            table = Sensors.objects.filter(pk=int(cd['sensor_id'][0])).using('global')
            req.session['selected_sensor'] = int(cd['sensor_id'][0])
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
        self.person_form = AddPerson()
        self.action_list = list(Maintenanceactions.objects.all().using('global').values_list('label', 'value'))
        self.sensor_list = list(Sensors.objects.all().using('global'))

    def get(self, req):
        return render(req, 'dashboard/admin.html', {'action_form': self.action_form, 'action_list': self.action_list, 'sensor_list': self.sensor_list, 'person_form': self.person_form})

    def post(self, req):
        if 'add_action' in req.POST:
            action_form = AddAction(req.POST)
            if action_form.is_valid():
                cd = action_form.cleaned_data
                action = Maintenanceactions(label=cd['action'], value=cd['action'])
                action.save(using='global')
                self.action_list = list(Maintenanceactions.objects.all().using('global').values_list('label', 'value'))
                return render(req, 'dashboard/admin.html', {'action_form': self.action_form, 'action_list': self.action_list, 'sensor_list': self.sensor_list})
        elif 'remove_action' in req.POST:
            to_remove = req.POST['remove_action']
            print(to_remove)
            Maintenanceactions.objects.filter(label=to_remove).using('global').delete()
            self.action_list = list(Maintenanceactions.objects.all().using('global').values_list('label', 'value'))
            return render(req, 'dashboard/admin.html',
                              {'action_form': self.action_form, 'action_list': self.action_list, 'sensor_list': self.sensor_list})
        elif 'add_person' in req.POST:
            person_form = AddPerson(req.POST)
            if person_form.is_valid():
                cd = person_form.cleaned_data
                person = People(first_name=cd['first_name'], last_name=cd['last_name'], email=cd['email'],
                                technician_czu=cd['technician_czu'], technician_company=cd['technician_company'],
                                sensor_type_id=int(cd['sensor_type'][0]))
                person.save(using='global')
                return render(req, 'dashboard/admin.html', {'action_form': self.action_form, 'action_list': self.action_list, 'sensor_list': self.sensor_list, 'person_form': self.person_form})


        return render(req, 'dashboard/admin.html',
                          {'action_form': self.action_form, 'action_list': self.action_list, 'sensor_list': self.sensor_list, 'person_form': self.person_form})


