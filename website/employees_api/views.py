# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import JsonResponse
from django.http import HttpResponse  # TODO:REMOVE ME
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict

from .models import Employee


@csrf_exempt
@require_http_methods(['GET'])
def list_employees(request):
    """Models the REST endpoint to list employees.

    Example
    -------
    Supposing the app is running on localhost, a GET request as
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


@require_http_methods(['DELETE'])
def delete_employee(request, employee_email):
    return HttpResponse('Delete employee %s' % employee_email)


def update_employee(request, employee_email):
    return HttpResponse('Update employee %s' % employee_email)
