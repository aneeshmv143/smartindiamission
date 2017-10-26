# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from main.models import UserProfile
from course.models import Course


class ChiefFunctionary(models.Model):
    center = models.ForeignKey(UserProfile)
    name = models.CharField(max_length=255, null=True, blank=True)
    designation = models.CharField(max_length=255, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    mobile_no = models.CharField(max_length=24, null=True, blank=True)

    def __str__(self):
        return str(self.center)


class CenterCourse(models.Model):
    center = models.ForeignKey(UserProfile)
    course = models.ForeignKey(Course)
    date_registered = models.DateField(auto_now=True)
    is_approved = models.BooleanField(default=False)
    date_approved = models.DateField(null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return str(self.center) + '-' + str(self.course)
