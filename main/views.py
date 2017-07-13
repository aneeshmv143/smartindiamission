# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import *
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.template.context_processors import csrf

from django.core.urlresolvers import reverse

from course.models import CourseCategory, Course, CourseSubject
from main.models import UserProfile

from smartmissionconfig.user_types import UserType

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
	response.update(csrf(request))
	response.update({'course_categories': CourseCategory.objects.all()})
	if request.method == 'GET':
		return render_to_response('login.html', response)
	if request.method == 'POST':
		username = request.POST.get('email', '')
		password = request.POST.get('password', '')
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				auth_login(request,user)
				try:
					user_profile = UserProfile.objects.get(user=user)
				except:
					raise Http404('No User Profile')
				if user_profile.user_type == UserType.types['Admin']:
					return HttpResponseRedirect(reverse('siteadmin:dashboard'))

			else:
				return HttpResponse('Inactice User')

		else:
			return HttpResponse('No User')

# Logout user
def logout(request):
    response = {}
    response.update(csrf(request))
    try:
        userprofile = UserProfile.objects.get(user=request.user)
    except:
        pass

    auth_logout(request)
    #response.update({'logout':True})
    return HttpResponseRedirect('/')			

#Course Details
def course_details(request, pk):
	response = {}
	response.update({'course_categories': CourseCategory.objects.all()})

	course = get_object_or_404(Course, pk=pk)
	response.update({'course': course})
	response.update({'course_details': CourseSubject.objects.filter(course=course)})
	return render_to_response('course_details.html', response)    