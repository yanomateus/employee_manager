# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import JsonResponse
from django.http import HttpResponse  # TODO:REMOVE ME
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict

from django.core.exceptions import ObjectDoesNotExist

from .models import Employee


EMPLOYEE_NOT_FOUND_JSON = {'error': 'employee not found'}
EMPLOYEE_DELETE_SUCCESS_JSON = {'msg': 'deleted'}


@csrf_exempt
@require_http_methods(['GET'])
def list_employees(request):
    """Implement the REST endpoint to list employees.

    Example
    -------
    Supposing the app is running on localhost:8000, a GET request as
        $ curl -X GET -H "application/json"  https://localhost:8000/employee/
    should return a json response like
        $ [
        $   {
        $     "name": "Ivisívis",
        $     "email": "ivis@sivis.com",
        $     "department": "Transparency"
        $   }
        $ ]
    """
    employees_list = [model_to_dict(emp, exclude=['id'])
                      for emp in Employee.objects.all()]
    return JsonResponse(employees_list,
                        safe=False,
                        json_dumps_params={'ensure_ascii': False})


@csrf_exempt
@require_http_methods(['DELETE'])
def delete_employee(request, employee_email):
    """Implement the REST enpoint to delete an employee.

    Example
    -------
    Supposing the app is running on localhost:8000, a DELETE request as
        $ curl -X DELETE -H "application/json" https://localhost:8000/employee \
        $   /foo@bar.com/delete/
    should return a json response like
        $ {'msg': 'deleted'}
    in case the user with email addres "foo@bar.com" exists. Otherwise it will
    a json response like
        $ {'error': 'employee not found'}
    """
    try:
        employee = Employee.objects.get(email=employee_email)
    except ObjectDoesNotExist:
        return JsonResponse(EMPLOYEE_NOT_FOUND_JSON)
    else:
        employee.delete()
        return JsonResponse(EMPLOYEE_DELETE_SUCCESS_JSON)


def update_employee(request, employee_email):
    return HttpResponse('Update employee %s' % employee_email)
