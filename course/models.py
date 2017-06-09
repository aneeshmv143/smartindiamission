# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# Category in which each course belongs
class CourseCategory(models.Model):
	title = models.CharField(max_length=255)
	description = models.TextField(null=True, blank=True)

	def __str__(self):
		return self.title

#Course Duration
class CourseDuration(models.Model):
	duration = models.CharField(max_length=255)
	more_info = models.TextField(null=True, blank=True)
	def __str__(self):
		return self.duration

#Course 
class Course(models.Model):
	category = models.ForeignKey(CourseCategory, on_delete=models.CASCADE)
	code = models.CharField(max_length=255)
	name = models.CharField(max_length=255)
	duration = models.ForeignKey(CourseDuration)
	description = models.TextField(null=True, blank=True)

	def __str__(self):
		return self.category.title +'->' + self.name

		