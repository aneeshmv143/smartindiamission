# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from course.models import CourseCategory, CourseDuration, Course
# Register your models here.
admin.site.register(CourseCategory)
admin.site.register(Course)
admin.site.register(CourseDuration)