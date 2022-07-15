
from django.urls import path
from .views import datastream_api


urlpatterns = [
    path(r'datastream/', datastream_api, name='datastream_api'),
]
