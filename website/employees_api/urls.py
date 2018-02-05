from django.conf.urls import url

from .views import list_employees
from .views import update_employee
from .views import delete_employee


_UPDATE_USER_REGEXP_STR = \
    r'^(?P<employee_email>[\w.%_+-]+@[A-Za-z0-9.-_]+\.[A-Za-z]{2,4})/update/$'
_DELETE_USER_REGEXP_STR = \
    r'^(?P<employee_email>[\w.%_+-]+@[A-Za-z0-9.-_]+\.[A-Za-z]{2,4})/delete/$'


urlpatterns = [
    url(r'^$', list_employees),
    url(_UPDATE_USER_REGEXP_STR, update_employee),
    url(_DELETE_USER_REGEXP_STR, delete_employee)
]
