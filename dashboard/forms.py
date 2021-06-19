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
    sensor_group = forms.CharField(label='Sensor Group', widget=forms.Select(choices=SENSOR_GROUPS))
    sensor_id = forms.CharField(label='Sensor ID', widget=forms.Select(choices=ID))


class CalibrationDate(forms.Form):
    date = forms.DateField(widget=forms.SelectDateWidget)
    time = forms.DateField(widget=forms.DateInput(attrs={'class':'datepicker'}))


