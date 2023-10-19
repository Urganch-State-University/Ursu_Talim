from django.urls import path
from .views import *

urlpatterns=[
    path('',homeview,name='home'),
    path('transfers/',transfersview,name='transfers'),
    path('ajax_get_options/',ajax_get_options,name='ajax_get_options'),
]