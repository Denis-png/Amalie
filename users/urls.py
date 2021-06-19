from django.urls import path
from django.conf import settings
from django.contrib.auth.views import LogoutView

from .views import *

urlpatterns = [
    path('register/', Register.as_view(), name='register'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout')
]
