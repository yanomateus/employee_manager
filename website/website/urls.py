from django.conf.urls import url
from django.conf.urls import include
from django.contrib import admin

urlpatterns = [
    url(r'^employee/', include('employees_api.urls')),
    url(r'^admin/', admin.site.urls)
]
