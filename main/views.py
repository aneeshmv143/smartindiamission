# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import *

from course.models import CourseCategory, Course

# Create your views here.

def index(request):
	response = {}
	response.update({'course_categories': CourseCategory.objects.all()})
	return render_to_response('index.html', response)


def about(request):
	response = {}
	response.update({'course_categories': CourseCategory.objects.all()})
	return render_to_response('about.html', response)

def objectives(request):
	response = {}
	response.update({'course_categories': CourseCategory.objects.all()})
	return render_to_response('objectives.html', response)	

def workplan(request):
	response = {}
	response.update({'course_categories': CourseCategory.objects.all()})
	return render_to_response('workplan.html', response)

def course_list(request, pk):
	response = {}
	response.update({'course_categories': CourseCategory.objects.all()})
	category = get_object_or_404(CourseCategory, pk=pk)
	response.update({'category': category})
	response.update({'courses': Course.objects.filter(category=category)})
	return render_to_response('course_list.html', response)		\

def contact(request):
	response = {}
	response.update({'course_categories': CourseCategory.objects.all()})
	return render_to_response('contact.html', response)

def registration(request):
	response = {}
	response.update({'course_categories': CourseCategory.objects.all()})	
	return render_to_response('registration.html', response)

def login(request):
	response = {}
	response.update({'course_categories': CourseCategory.objects.all()})
	if request.method == 'GET':
		return render_to_response('login.html', response)
	else:
		raise Http404	