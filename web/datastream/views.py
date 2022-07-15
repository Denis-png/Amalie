from django.shortcuts import render
from dashboard.models import Api, Condition, Group, Maintenance, Maintenanceactions, People, Project, SensorType,\
    SensorVariable, Sensors, SensorsGroup, Variables, DataCleverfarm, DataEmsbrno, DataEkotechnika, DataTomst, DataVrty
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.apps import apps
import json


@csrf_exempt
def datastream_api(request):
    """ responding according to request settings """
    try:
        req_type = request.GET.get('type')

        if req_type == 'tables-list':
            app_models_dirty = list(apps.get_app_config('dashboard').get_models())
            app_models_clean = []
            app_tables = []
            for model in app_models_dirty:
                app_models_clean.append(model.__name__)
            for model in app_models_dirty:
                app_tables.append(model._meta.db_table)
            json_resp = {'resp_status': '200', 'list_of_models': app_models_clean, 'list_of_tables': app_tables}
            return JsonResponse(json_resp)

        elif req_type == 'tables-data':
            req_table_name = request.GET.get('model-name')
            desired_model = apps.get_model(app_label='dashboard', model_name=f'{req_table_name}')
            num_of_rows_to_display = 10 if int(request.GET.get('nrows')) >= 10 else int(request.GET.get('nrows'))
            resp_models_data = list(desired_model.objects.order_by('id').all()[:num_of_rows_to_display].values().using('global'))
            json_resp = {'resp_status': '200', 'db_data': resp_models_data}
            return JsonResponse(json_resp)
        else:
            json_resp = {'resp_status': '400',
                         'resp_message': 'Request setting is wrong. Fix it or contact dev department.'}
            return JsonResponse(json_resp)

    except Exception as err:
        print(f'During datastream_api error accured: {err}')
        json_resp = {'resp_status': '400', 'resp_message': 'Something went wrong. Please contact dev department.'}
        return JsonResponse(json_resp)
