# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.shortcuts import *
from django.template.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.core import serializers 

from django.contrib.auth.models import User

from main.models import UserProfile
from course.models import Course, CourseCategory, CourseDuration

from smartmissionconfig.user_types import UserType

from siteadmin.forms import CourseForm

def admin_check(user):
	user_profile = get_object_or_404(UserProfile, user=user)
	return user_profile.user_type == UserType.types['Admin']

@login_required
@user_passes_test(admin_check)
def dashboard(request):
	response = {}
	response.update({'user_profile': get_object_or_404(UserProfile, user=request.user)})
	response.update({'course':Course.objects.count()})
	return render_to_response('siteadmin_dashboard.html', response)

@login_required
@user_passes_test(admin_check)
def course_list(request):
	response = {}
	response.update({'user_profile': get_object_or_404(UserProfile, user=request.user)})
	response.update({'course_categories': CourseCategory.objects.all()})
	return render_to_response('siteadmin_course_list.html', response)

@login_required
@user_passes_test(admin_check)
def ajax_courses(request):
	if 'course_category' in request.GET and request.GET['course_category']:
		course_category_id = request.GET['course_category']
	else:
		raise Http404()
	course_category = get_object_or_404(CourseCategory, pk=course_category_id)
	return HttpResponse(
		serializers.serialize(
			'json',
			Course.objects.filter(category=course_category).order_by('id')
		)
	)	

@login_required
@user_passes_test(admin_check)
def course_edit(request):
	response = {}
	response.update({'user_profile': get_object_or_404(UserProfile, user=request.user)})
	response.update(csrf(request))
	response.update({'course_categories': CourseCategory.objects.all()})
	response.update({'course_duration': CourseDuration.objects.all()})
	if request.method == 'GET':
		if 'course' in request.GET and request.GET['course']:
			course_id = request.GET['course']
		else:
			raise Http404
		course = get_object_or_404(Course, pk=course_id)
		response.update({'course':course})
		return render_to_response('siteadmin_course_edit.html', response)
	if request.method == 'POST':
		form = CourseForm(request.POST)
		if form.is_valid():
			response.update({'form': form})
			course_id = request.POST.get('course', '')
			course = get_object_or_404(Course, pk=course_id)
			course.category = get_object_or_404(CourseCategory, pk=form.cleaned_data['course_category'])
			course.code = form.cleaned_data['course_code']
			course.name = form.cleaned_data['course_name']
			course.duration = get_object_or_404(CourseDuration, pk=form.cleaned_data['course_duration'])
			try:
				course.save()
			except:
				raise Http404
			else:
				response.update({'course_edited':True})
				return render_to_response('siteadmin_course_list.html', response)	
		else:
			return HttpResponse('Form Error')