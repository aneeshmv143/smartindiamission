# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
#Country
class Country(models.Model):
	country = models.CharField(max_length=255)
	country_name = models.SlugField(db_index=True)

	def __str__(self):
		return str(self.country)

#State
class State(models.Model):
	country = models.ForeignKey(Country)
	state = models.CharField(max_length=255)
	state_name = models.SlugField(db_index=True)

	def __str__(self):
		return str(self.country.country) + '->' + str(self.state)

#District
class District(models.Model):
	state = models.ForeignKey(State)
	district = models.CharField(max_length=255)
	district_name = models.SlugField(db_index=True)

	def __str__(self):
		return str(self.state.country.country) + '->' + str(self.state.state) + '->' + str(self.district)
