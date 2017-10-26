# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.

from static_data.models import Country, State, District

admin.site.register(Country)
admin.site.register(State)
admin.site.register(District)
