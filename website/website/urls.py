from django.conf.urls import url
from django.conf.urls import include
from django.contrib import admin

from .views import index

urlpatterns = [
    url(r'^$', index),
    url(r'^employee/', include('employees_api.urls')),
    url(r'^admin/', admin.site.urls)
]
