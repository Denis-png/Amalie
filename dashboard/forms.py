from django import forms
from django.contrib.gis import forms
from django.forms import widgets, ModelForm
from .models import *

from .models import *

SENSOR_GROUPS = [
    ('all','------'),
    ('test','Test'),
]

ID = [
    ('test','Test'),
    ('21101902', 'BP I/1 puda10'),
]




class SelectSensor(forms.Form):
    sensor_group = forms.CharField(label='Sensor Group', widget=forms.Select(attrs={'class': 'form-select form-select-sm'}, choices=SENSOR_GROUPS))
    sensor_id = forms.CharField(label='Sensor ID', widget=forms.Select(attrs={'class': 'form-select form-select-sm'}, choices=ID))


class AddAction(forms.Form):
    action = forms.CharField(label='', max_length=255, widget=forms.TextInput(attrs={'class': 'form-control mb-3'}))


class AddSensorForm(ModelForm):
    class Meta:
        model = Sensors
        fields = ['sensor_id', 'sensor_name', 'company', 'measured_quantity', 'calibration_interval', 'units']

        widgets = {
            'sensor_id': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'sensor_name': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'company': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'measured_quantity': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'calibration_interval': forms.NumberInput(attrs={'class': 'form-control mb-3'}),
            'units': forms.TextInput(attrs={'class': 'form-control mb-3'})
        }



