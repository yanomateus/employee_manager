# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Employee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    department = models.CharField(max_length=100)

    def __str__(self):
        return self.email
