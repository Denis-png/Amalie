from django.urls import path
from .views import *
from .dash_apps.finished import calibration_form, maintenance, permissions

urlpatterns = [
    # GENERAL PATH
    path('', DashboardView.as_view(), name='dashboard'),

    # SENSORS URLS
    path('sensors/', SensorsView.as_view(), name='sensors_dashboard'),

    # DATA QUALITY URLS
    path('data/', DataQView.as_view(), name='data_dashboard'),

    # HISTORY PATH
    path('history/', HistoryView.as_view(), name='history_dashboard'),

    # ADMIN PAGE URL
    path('admin/', AdminView.as_view(), name='admin_page'),
]