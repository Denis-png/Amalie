from django.urls import path
from .views import *
from .dash_apps.finished import sensors

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('sensors/', SensorsView.as_view(), name='sensors_dashboard'),
    path('data/', DataQView.as_view(), name='data_dashboard'),
    path('history/', HistoryView.as_view(), name='history_dashboard'),
]