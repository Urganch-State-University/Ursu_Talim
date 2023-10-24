from django.urls import path
from .views import *

urlpatterns=[
    path('',transfersview,name='transfers'),
    path('ajax_get_options/',ajax_get_options,name='ajax_get_options'),
    path('showgpa/',showgpaview,name='showgpa'),
    path('showmainform/',showmainformview,name='showmainform'),
    path('download_gpa_pdf/',DownloadPDF.as_view(),name='download_gpa_pdf'),
    path('show_gpa_pdf/',ViewPDF.as_view(),name='show_gpa_pdf'),
]