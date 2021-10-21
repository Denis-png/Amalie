from django.urls import path
from .views import *


urlpatterns = [
    # GENERAL PATH
    path('', DashboardView.as_view(), name='dashboard'),

    # QUERY URLS
    path('query/', QueryView.as_view(), name='query'),
    path('query/save/', save_data, name='save_data'),


    # MAINTENANCE URLS
    path('maintenance/', MaintenanceView.as_view(), name='maintenance_sensor'),
    path('maintenance/add_new', maintenance, name='maintenance'),
    path('maintenance/update_actions', update_actions, name='update_actions'),
    path('maintenance/condition', condition, name='condition'),

    # USERS PATH
    path('users/', UsersView.as_view(), name='users'),

    # ADMIN PAGE URL
    path('admin/', AdminView.as_view(), name='admin_page'),
]
