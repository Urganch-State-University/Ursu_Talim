
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('home.urls')),
    path('transfers/',include('transfers.urls')),
    # path('accounts/',include('accounts.urls')),
    path('accounts/',include('django.contrib.auth.urls')),

]
