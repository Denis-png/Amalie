from django.urls import path
from .views import *
from .dash_apps.finished import plot

urlpatterns = [
    path('select/', Select.as_view(), name='select'),
    path('save/', save_data, name='save'),
]