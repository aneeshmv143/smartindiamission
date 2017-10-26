# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

from static_data.models import District


# Create your models here.
class UserProfile(models.Model):
    user = models.ForeignKey(User)
    gender = models.CharField(max_length=2, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    address1 = models.TextField(null=True, blank=True)
    address2 = models.TextField(null=True, blank=True)
    district = models.ForeignKey(District, null=True, blank=True)
    pincode = models.CharField(max_length=10, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    user_type = models.CharField(max_length=2, blank=True)
    added_by = models.CharField(max_length=50, null=True, blank=True)
    plain_password = models.CharField(max_length=50, null=True, blank=True)
    profile_pic = models.CharField(max_length=255, null=True, blank=True)
    is_paid = models.BooleanField(default=False)
    renew_date = models.DateField(null=True, blank=True)
    reg_no = models.CharField(max_length=255, null=True, blank=True)
    reg_date = models.CharField(max_length=255, null=True, blank=True)
    website = models.CharField(max_length=255, null=True, blank=True)
    nature = models.CharField(max_length=100, null=True, blank=True)
    mobile_no = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.user.username


# Contact Message
class ContactMessage(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    contact_no = models.CharField(max_length=255, null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    date = models.DateField(auto_now=True)

    def __str__(self):
        return self.name


# Activation Key
class UserActivation(models.Model):
    user = models.ForeignKey(User)
    key = models.CharField(max_length=255)
    date = models.DateField(auto_now=True)

    def __str__(self):
        return self.user.first_name
