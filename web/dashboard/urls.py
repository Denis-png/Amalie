from django.urls import path
from .views import *


urlpatterns = [



    # DASHBOARD URLs
    path('dashboard/', DashboardView.as_view(), name='dashboard'),

    # SENSORS URLs
    path('sensors/', SensorsView.as_view(), name='sensors'),
    path('sensors/maintenance', maintenance, name='maintenance'),
    path('sensors/condition', condition, name='condition'),
    path('sensors/get_sensor_info/', get_sensor_info, name='get_sensor_info'),

    # ADMIN URLs
    path('admin/', AdminView.as_view(), name='admin_page'),
    path('admin/update_actions/', update_actions, name='update_actions'),

    # SUPPORT URLs
    path('support/', SupportView.as_view(), name='support_page'),
    
    
]
