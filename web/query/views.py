import csv
import json

from django.apps import apps
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import *
from django.views import View


features = [x for x in apps.get_app_config('query').get_models()]


# SELECTION RENDER

class Select(View):
    def __init__(self):
        self.select = SelectFeature()
        self.save = Save()

    @method_decorator(login_required)
    def get(self, req):
        print(features)
        return render(req, '../templates/query/selection_page.html', {'select': self.select})

    @method_decorator(login_required)
    def post(self, req):
        params = SelectFeature(req.POST)
        if params.is_valid():
            cd = params.cleaned_data
            for feature in features:
                print(feature)
                if cd['feature'] == feature.__name__:
                    data = feature.objects.filter(date__gt=cd['date_from'], date__lt=cd['date_to']).using('global')
            req.session['data'] = json.dumps(list(data.values()), cls=DjangoJSONEncoder)
            req.session['django_plotly_dash'] = json.dumps(list(data.values()), cls=DjangoJSONEncoder)
        return render(req, '../templates/query/selection_page.html',
                      {'data': data.values(), 'save': self.save, 'title': cd['feature'], 'select': params,
                       'dash': {cd['feature']: data.values()}})


@login_required
def save_data(req):
    if req.method == 'POST':
        save = Save(req.POST)
        if save.is_valid():
            cd = save.cleaned_data
            if cd['format'] == 'csv':
                data = json.loads(req.session.get('data'))
                res = HttpResponse(content_type='text/csv')
                res['Content-Disposition'] = 'attachment; filename="data.csv"'
                writer = csv.writer(res)
                writer.writerow(['id', 'sensor_name', 'date', 'time', 'value', 'signal'])
                for row in data:
                    writer.writerow(row.values())
            elif cd['format'] == 'json':
                data = json.loads(req.session.get('data'))
                save_dt = json.dumps(data)
                res = HttpResponse(save_dt, content_type='application/json')
                res['Content-Disposition'] = 'attachment; filename="data.json"'
            return res
