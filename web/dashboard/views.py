import json
from django.shortcuts import render, redirect
from django.views import View
from .models import *
from django.apps import apps
from django.db import connection
from django.db.models import Max
from datetime import datetime, timedelta
from django.views.decorators import csrf
from django.utils.decorators import method_decorator
from django.http import JsonResponse
import pandas as pd


# DASHBOARD HOME VIEW
@method_decorator(csrf.csrf_exempt, name='dispatch')
class DashboardView(View):
    def __init__(self):
        self.ctx = {}


    def get(self, req): 

        # Logging terminal output
        log_file = open('../python/logs/daily.txt', 'r')
        self.ctx['companies'] = (json.loads(log_file.read()))
        log_file.close()

        return render(req, '../templates/dashboard/dashboard.html', self.ctx)

    
    def post(self, req):

        # Get dashboard data for charts by company 
        company = req.POST.get('company')

        # Data table name
        self.ctx['dt_name'] = f'data_{company}'
        model = apps.get_model(app_label='dashboard', model_name=f'Data{company}')

        # N rows
        self.ctx['n_rows'] = model.objects.all().using('global').count()

        # Data table size (kb, mb)
        # with connection.cursor() as c:
        #     c.execute(f"SELECT pg_size_pretty(pg_total_relation_size('global.data_{company}'))")
        #     self.ctx['dt_size'] = c.fetchall()[0][0]

        # Date range chart for sensors
        end_date = datetime.now().date()
        start_date = end_date.replace(day=1, month=1)
        
        #daterange = pd.date_range(start=start_date, end=end_date)

        sensors = list(Sensors.objects.using('global').filter(company=company.title()).values_list('id', 'sensor_name'))
        
        labels = [x[1] for x in sensors]

        dates = []
        for sensor in sensors:
            dates.append(model.objects.using('global').filter(sensor_id=sensor[0]).aggregate(Max('date'))['date__max'])

        

        self.ctx['chart_data'] = {'data': dates, 'labels': labels, 'min_date':start_date}

        # Daily console output 
        
        


        return JsonResponse(self.ctx)



# Sensors VIEW
class SensorsView(View):
    def __init__(self):
        self.ctx = dict()
        self.ctx['sensors'] = Sensors.objects.all().using('global').values('id', 'sensor_name')
        self.ctx['actions'] = list(Maintenanceactions.objects.all().using('global').values('label', 'value'))
        self.ctx['users'] = list(People.objects.all().using('global').values('id', 'first_name', 'last_name'))

    def get(self, req):
        return render(req, '../templates/dashboard/sensors.html', self.ctx)

    def post(self, req):
        
        return render(req, '../templates/dashboard/sensors.html', self.ctx)


@csrf.csrf_exempt
def maintenance(req):
    user_id = req.POST.get('maintenance_user')
    print(user_id)
    action = req.POST.get('maintenance_action')
    date = req.POST.get('maintenance_datetime').split(' ')[0]
    time = req.POST.get('maintenance_datetime').split(' ')[1]
    note = req.POST.get('maintenance_note')
    sensor_id = req.POST.get('sensor_id')

    new = Maintenance(date=date, time=time, user_id=user_id, action=action, note=note, sensor_id=sensor_id)
    new.save(using='global')

    return JsonResponse({'msg': f"Maintenance action for {sensor_id} was successfully inserted."})

    

@csrf.csrf_exempt
def condition(req):
    start_date = req.POST.get('condition_date_start').split(' ')[0]
    start_time = req.POST.get('condition_date_end').split(' ')[1]
    end_date = req.POST.get('condition_date_start').split(' ')[0]
    end_time = req.POST.get('condition_date_end').split(' ')[1]
    condition = req.POST.get('condition_state')
    note = req.POST.get('condition_note')
    sensor_id = req.POST.get('sensor_id')

    print(sensor_id)

    new = Condition(start_date=start_date, start_time=start_time, end_date=end_date, end_time=end_time, condition=condition, note=note, sensor_id=sensor_id)
    new.save(using='global')

    return JsonResponse({'msg': f"Maintenance action for {sensor_id} was successfully inserted."})

@csrf.csrf_exempt
def get_sensor_info(req):
    
    # Get sensor stats and info by ID
    sensor_id = req.POST.get('chosen_sensor')
    
    
    # Sensor name and Serial number
    sensor = list(Sensors.objects.filter(id=sensor_id).using('global').values('sensor_name', 'serial_number'))
    
    company = list(Sensors.objects.filter(id=sensor_id).using('global').values('company'))[0]['company']
    
    data_model = apps.get_model(app_label='dashboard', model_name=f'Data{company}')
    
    variable_id = list(data_model.objects.using('global').filter(sensor_id=sensor_id).values('variable_id').distinct())

    variables = []

    for var in variable_id:
        var_name = Variables.objects.using('global').get(id=var['variable_id'])
        variables.append(var_name.name)


    latest = list(data_model.objects.using('global').filter(sensor_id=sensor_id, variable_id=variable_id[0]['variable_id']).values('date').order_by('date'))[0]['date']
    
    records = list(Maintenance.objects.filter(sensor_id=sensor_id).using('global').values('date', 'time', 'action'))
    records_str = [f"{x['date']} {x['time']} | {x['action']}" for x in records]


    response_data = {'id': sensor_id, 'sensor_name': sensor[0]['sensor_name'], 'serial': sensor[0]['serial_number'],
                     'variables': sorted(variables), 'latest_record': latest, 'records': records_str}


    return JsonResponse(response_data)




# ADMIN VIEW
class AdminView(View):
    def __init__(self):
        self.ctx = {}
        self.ctx['actions'] = list(Maintenanceactions.objects.all().using('global').values('value', 'label'))

    def get(self, req):
        
        return render(req, '../templates/dashboard/admin.html', self.ctx)

    def post(self, req):
        return render(req, '../templates/dashboard/admin/admin.html',
                      {'action_form': self.action_form, 'action_list': self.action_list,
                       'sensor_list': self.sensor_list, 'person_form': self.person_form})


def update_actions(req):
    if req.POST.get('to_remove'):
        to_remove = req.POST.get('to_remove')
        Maintenanceactions.objects.filter(label=to_remove).using('global').delete()
    if req.POST.get('to_add'):
        label_value = req.POST.get('to_add')
        new_action = Maintenanceactions(label=label_value, value=label_value)
        new_action.save(using='global')
    return redirect('/admin/')


class SupportView(View):
    def __init__(self):
        pass

    def get(self, req):
        pass

    def post(self, req):
        pass

