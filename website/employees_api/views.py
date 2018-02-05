# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse  # TODO:replace by JsonResonse


def list_employees(request):
    return HttpResponse('return list of employees')


def delete_employee(request, employee_email):
    return HttpResponse('Delete employee %s' % employee_email)


def update_employee(request, employee_email):
    return HttpResponse('Update employee %s' % employee_email)
