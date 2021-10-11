from django import forms
from django.urls import reverse

FEATURES = [
    ('all', '---------'),
    ('Swp', 'Soil water potential'),
    ('Tmp', 'Temperature'),
    ('Hum', 'Humidity'),
    ('Prs','Pressure'),
    ('Rnf','Rainfall'),
    ('Lfw','Leaf Wetness'),
    ('Wnd','Wind direction'),
    ('Wns','Wind speed'),
    ('Wng','Wind gust'),
]


formats = [
    ('csv','CSV'),
    ('json','JSON'),
]


class SelectFeature(forms.Form):
    feature = forms.CharField(label='Feature', widget=forms.Select(attrs={'class': 'form-select'}, choices=FEATURES), required=True)
    date_from = forms.DateField(widget=forms.SelectDateWidget(attrs={'class': 'form-select form-select-sm'}))
    date_to = forms.DateField(widget= forms.SelectDateWidget(attrs={'class': 'form-select form-select-sm'}))


class Save(forms.Form):
    format = forms.CharField(label='Format', widget=forms.Select(attrs={'class': 'form-select form-select-sm w-25 ml-3'}, choices=formats), required=False)


