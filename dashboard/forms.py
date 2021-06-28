from django import forms
from django.forms import widgets

from .models import *

SENSOR_GROUPS = [
    ('all','------'),
    ('test','Test'),
]

ID = [
    ('test','Test'),
]


class SelectSensor(forms.Form):
    sensor_group = forms.CharField(label='Sensor Group', widget=forms.Select(attrs={'class': 'form-select form-select-sm'}, choices=SENSOR_GROUPS))
    sensor_id = forms.CharField(label='Sensor ID', widget=forms.Select(attrs={'class': 'form-select form-select-sm'}, choices=ID))


class AddAction(forms.Form):
    action = forms.CharField(label='', max_length=255, widget=forms.TextInput(attrs={'class': 'form-control mb-3'}))


