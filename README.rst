===============================
Employee management application
===============================

This is a simple `Django <https://www.djangoproject.com/>`_ powered REST API to manage employee data.

requirements
------------
* python 2.7.9
* pip 9.0.1
* django 1.11.10

getting started
---------------
* Fork this respository and clone your fork::

    user@machine~$ git clone https://github.com/yanomateus/employee_manager.git

* Install the requirements (you might want to do this inside a virtualenv)::

    user@machine~$ cd employee_manager
    user@machine~/employee_manager$ pip install -r requirements.txt

* Run the required migrations to initialize a SQLite database::

    user@machine~/employee_manager$ cd website
    user@machine~/employee_manager/website$ python manager.py migrate

* Start the development server, which you can then access on ``http://localhost:8000``::

    user@machine~/employee_manager/website$ python manager.py runserver
