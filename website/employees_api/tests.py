# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist
from .models import Employee
from .views import MISSING_DATA_JSON
from .views import EMPLOYEE_EMAIL_NOT_AVAILABLE_JSON
from .views import EMPLOYEE_NOT_FOUND_JSON
from .views import EMPLOYEE_UPDATE_SUCEESS_JSON
from .views import EMPLOYEE_CREATED_JSON
from .views import EMPLOYEE_DELETE_SUCCESS_JSON


class TestCreateEmployeeRESTEndpoint(TestCase):
    """Test POST /employee/create endpoint."""

    def test_proper_employee_creation(self):
        """
        Send POST request with mock data and ensures the saved data matches the
        provided data.
        """
        mock_employee = {
            'name': 'emp_name',
            'email': 'emp@mail.com',
            'department': 'emp_department'
        }
        response = self.client.post('/employee/create/',
                                    json.dumps(mock_employee),
                                    content_type='application/json')
        last_employee = Employee.objects.last()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), EMPLOYEE_CREATED_JSON)
        self.assertEqual(last_employee.name, mock_employee['name'])
        self.assertEqual(last_employee.email, mock_employee['email'])
        self.assertEqual(last_employee.department, mock_employee['department'])

    def test_proper_response_on_missing_data(self):
        """Send faulty data and expect json with error to be returned."""
        faulty_data = {
            'name': 'emp_name',
            'department': 'emp_department'
        }  # email param is missing
        response = self.client.post('/employee/create/',
                                    json.dumps(faulty_data),
                                    content_type='application/json')
        self.assertEqual(response.json(), MISSING_DATA_JSON)

    def test_proper_response_on_not_available_email(self):
        """Send data with not-available email address and expect json error."""
        emp = Employee()
        emp.name = 'emp'
        emp.email = 'emp@mail.com'
        emp.department = 'emp_department'
        emp.save()

        employee_data = {
            'name': 'other_emp',
            'email': 'emp@mail.com',  # problematic data
            'department': 'emp_department'
        }

        response = self.client.post('/employee/create/',
                                    json.dumps(employee_data),
                                    content_type='application/json')
        self.assertEqual(response.json(), EMPLOYEE_EMAIL_NOT_AVAILABLE_JSON)


class TestUpdateEmployeeRESTEndpoint(TestCase):
    """Test PUT /employee/<email>/update."""

    def test_proper_employee_update(self):
        """Test proper data update."""
        emp = Employee()
        emp.name = 'emp'
        emp.email = 'emp@mail.com'
        emp.department = 'emp_department'
        emp.save()

        resp = self.client.put('/employee/emp@mail.com/update/',
                               data='{"name":"new_name"}')  # update name

        updated_emp = Employee.objects.last()
        self.assertEqual(resp.json(), EMPLOYEE_UPDATE_SUCEESS_JSON)
        self.assertEqual(updated_emp.name, 'new_name')


    def test_proper_error_response_on_email_not_available(self):
        """Test json error obj return when email address is already in use."""
        emp1 = Employee()
        emp1.name = 'emp'
        emp1.email = 'emp1@mail.com'
        emp1.department = 'dep'
        emp1.save()

        emp2 = Employee()
        emp2.name = 'emp2'
        emp2.email = 'emp2@mail.com'
        emp2.department = 'dep'
        emp2.save()

        resp = self.client.put('/employee/emp2@mail.com/update/',
                               data='{"email":"emp1@mail.com"}')
        self.assertEqual(resp.json(), EMPLOYEE_EMAIL_NOT_AVAILABLE_JSON)

    def test_proper_error_response_on_employee_not_found(self):
        """Test json error obj return when employee is not found."""
        resp = self.client.put('/employee/xxxxxxxxxx@xxxxxxxxxxx.com/update/',
                               data='{"name":"new_name"}')
        self.assertEqual(resp.json(), EMPLOYEE_NOT_FOUND_JSON)


class TestEmployeeDeleteRESTEndpoint(TestCase):
    """Test DELETE /employee/<email>/delete."""

    def test_proper_employee_delete(self):
        """Test if employee is properly deleted."""
        emp = Employee()
        emp.name = 'emp'
        emp.email = 'emp@mail.com'
        emp.department = 'dep'
        emp.save()

        resp = self.client.delete('/employee/emp@mail.com/delete/')

        self.assertEqual(resp.json(), EMPLOYEE_DELETE_SUCCESS_JSON)
        with self.assertRaises(ObjectDoesNotExist):
            Employee.objects.get(email='emp@mail.com')

    def test_proper_error_return(self):
        """Test json error obj return when employee is not found."""
        resp = self.client.delete('/employee/xxxx@xxxx.com/delete/')
        self.assertEqual(resp.json(), EMPLOYEE_NOT_FOUND_JSON)


class TestEmployeeListRESTEndpoint(TestCase):
    """Test GET /employee/."""

    def test_trivial_employee_list_return(self):
        """Test if returned list is empty."""
        resp = self.client.get('/employee/')
        self.assertEqual(resp.json(), [])


    def test_proper_employee_list_return(self):
        """Test if added data is returned on list."""
        emp1 = Employee()
        emp1.name = 'emp1'
        emp1.email = 'emp1@mail.com'
        emp1.department = 'dep'
        emp1.save()

        emp2 = Employee()
        emp2.name = 'emp2'
        emp2.email = 'emp2@mail.com'
        emp2.department = 'dep'
        emp2.save()

        emp1_dict = {
            'name': emp1.name,
            'email': emp1.email,
            'department': emp1.department
        }
        emp2_dict = {
            'name': emp2.name,
            'email': emp2.email,
            'department': emp2.department
        }

        resp = self.client.get('/employee/')
        self.assertEqual(resp.json(), [emp1_dict, emp2_dict])
