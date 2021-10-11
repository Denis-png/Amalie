from django import forms
from django.contrib.gis import forms
from django.forms import widgets, ModelForm
from .models import *

from .models import *


def sensor_group():
    group_list = Group.objects.all().using('global').values_list('id', 'group_id')
    return group_list


def sensor():
    sensor_list = Sensors.objects.all().using('global').values_list('id', 'sensor_name')
    return sensor_list


def sensor_types():
    type_list = SensorType.objects.all().using('global').values_list('id', 'sensor_type_id')
    return type_list


class SelectSensor(forms.Form):
    sensor_group = forms.CharField(label='Sensor Group', widget=forms.Select(attrs={'class': 'form-select form-select-sm'}, choices=sensor_group()), required=False)
    sensor_id = forms.CharField(label='Sensor ID', widget=forms.Select(attrs={'class': 'form-select form-select-sm'}, choices=sensor()))


class AddAction(forms.Form):
    action = forms.CharField(label='', max_length=255, widget=forms.TextInput(attrs={'class': 'form-control mb-3'}))


class AddPerson(forms.Form):
    first_name = forms.CharField(label='First name', max_length=255)
    last_name = forms.CharField(label='Last name', max_length=255)
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'style': 'color: #2a5d68; border-color: #2a5d68;'}), required=True)
    technician_czu = forms.BooleanField(widget=forms.CheckboxInput(), required=False)
    technician_company = forms.BooleanField(widget=forms.CheckboxInput(), required=False)
    sensor_type = forms.MultipleChoiceField(choices=sensor_types())


'''
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
'''


