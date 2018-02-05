# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

from .models import Employee


EMPLOYEE_NOT_FOUND_JSON = {'error': 'employee not found'}
EMPLOYEE_DELETE_SUCCESS_JSON = {'msg': 'deleted'}
EMPLOYEE_UPDATE_SUCEESS_JSON = {'msg': 'updated'}
EMPLOYEE_EMAIL_NOT_AVAILABLE_JSON = {'error': 'email addess not available'}
EMPLOYEE_CREATED_JSON = {'msg': 'created'}
MISSING_DATA_JSON = {'error': 'missing data'}


@csrf_exempt
@require_http_methods(['GET'])
def list_employees(request):
    """Implement the REST endpoint to list employees.

    Example
    -------
    Supposing the app is running on localhost:8000, a GET request as::

        curl -X GET -H "application/json" http://localhost:8000/employee/

    should return a json response like::

        [
          {
            "name": "emp",
            "email": "emp@department.com",
            "department": "department_name"
          }
        ]

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
    Supposing the app is running on localhost:8000, a DELETE request as::

        curl -X DELETE -H "application/json"
            http://localhost:8000/employee/foo@bar.com/delete/

    should return a json response like::

        {'msg': 'deleted'}

    in case the user with email address "foo@bar.com" exists. Otherwise it will
    a json response like::

        {'error': 'employee not found'}

    """
    try:
        employee = Employee.objects.get(email=employee_email)
    except ObjectDoesNotExist:
        return JsonResponse(EMPLOYEE_NOT_FOUND_JSON)
    else:
        employee.delete()
        return JsonResponse(EMPLOYEE_DELETE_SUCCESS_JSON)


@csrf_exempt
@require_http_methods(['PUT'])
def update_employee(request, employee_email):
    """Implement REST endpoint to update an employee's data.

    Example
    -------
    Supposing the app is running on localhost:8000, a PUT request as::

        curl -X PUT -H "Content-Type: application/json"
          -d '{"name":"new_name", "email": "new@mail.com",
          "department": "new_department"}'
          http://localhost:8000/employee/b@b.com/update/

    should return a json response like::

        {'msg': 'updated'}

    if the employee exists and was succefully updated. If the employee doesn't
    exist it will return a json response like::

        {'error': 'employee not found'}

    If the request payload contains an email which is not available, then this
    endpoint will return a json response like::

        {'error': 'email addess not available'}

    """
    try:
        employee = Employee.objects.get(email=employee_email)
    except ObjectDoesNotExist:
        return JsonResponse(EMPLOYEE_NOT_FOUND_JSON)

    update_data = json.loads(request.body)
    if 'name' in update_data:
        employee.name = update_data['name']
    if 'department' in update_data:
        employee.department = update_data['department']
    if 'email' in update_data:
        employee.email = update_data['email']

    try:
        employee.save()
    except IntegrityError:
        return JsonResponse(EMPLOYEE_EMAIL_NOT_AVAILABLE_JSON)
    else:
        return JsonResponse(EMPLOYEE_UPDATE_SUCEESS_JSON)


@csrf_exempt
@require_http_methods(['POST'])
def create_employee(request):
    """Implement REST endpoint to create an employee.

    Example
    -------
    Supposing the app is running on localhost:8000, a request as::

        curl -X POST -H "Content-Type: application/json"
            -d '{"name": "emp_name", "department": "dep_name",
            "email": "emp_name@mail.com"}'
            http://localhost:8000/employee/create/

    should return a json response like::

        {'msg': 'created'}

    If required data is missing on the request's body then this endpoint will
    return a json reponse like::

        {'error': 'missing data'}

    If the email param passed is not available then this endpoint will return
    a json response like::

        {'error': 'email addess not available'}

    """
    employee_data = json.loads(request.body)
    try:
        assert ('name' in employee_data and
                'email' in employee_data and
                'department' in employee_data)
    except AssertionError:
        return JsonResponse(MISSING_DATA_JSON)

    new_employee = Employee()
    new_employee.name = employee_data['name']
    new_employee.email = employee_data['email']
    new_employee.department = employee_data['department']
    try:
        new_employee.save()
    except IntegrityError:
        return JsonResponse(EMPLOYEE_EMAIL_NOT_AVAILABLE_JSON)
    else:
        return JsonResponse(EMPLOYEE_CREATED_JSON)
