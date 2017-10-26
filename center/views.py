# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import *
from django.template.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

from smartmissionconfig.user_types import UserType

from center.forms import CenterProfileForm, FunctionaryForm

from main.models import UserProfile
from center.models import ChiefFunctionary, CenterCourse
from course.models import CourseCategory, Course
from static_data.models import State

import json


# Ajax for courses conducted by centers
def center_ajax_course(request):
    response = {}
    if 'course_category' in request.GET and request.GET['course_category']:
        course_category = request.GET['course_category']
    else:
        raise Http404
    category = get_object_or_404(CourseCategory, pk=course_category)
    courses = CenterCourse.objects.filter(course__category=category)
    response.update({'courses': courses})
    return render(request, 'center_ajax_courses.html', response)


def center_check(user):
    user_profile = get_object_or_404(UserProfile, user=user)
    return user_profile.user_type == UserType.types['Center']


# Center Dashboard View
@login_required
@user_passes_test(center_check)
def dashboard(request):
    response = {}
    user_profile = get_object_or_404(UserProfile, user=request.user)
    response.update({'center': user_profile})
    if user_profile.is_paid is True:
        return render(request, 'center_dashboard.html')
    else:
        return render(request, 'center_dashboard.html', response)


@login_required
@user_passes_test(center_check)
def center_profile(request):
    response = {}
    user_profile = get_object_or_404(UserProfile, user=request.user)
    response.update({'user_profile': user_profile})
    #chief_functionary = get_object_or_404(ChiefFunctionary, center=user_profile)
    #response.update({'chief_functionary': chief_functionary})
    response.update({'course_categories': CourseCategory.objects.all()})
    return render(request, 'center_profile.html', response)


# Update Center Info
@login_required
@user_passes_test(center_check)
def update_center_profile(request):
    response = {}
    response.update(csrf(request))
    user_profile = get_object_or_404(UserProfile, user=request.user)
    response.update({'user_profile': user_profile})
    response.update({'states': State.objects.all().order_by('pk')})
    if request.method == 'GET':
        return render(request, 'update_center_profile.html', response)
    if request.method == 'POST':
        form = CenterProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            center_name = request.POST.get('center_name', '')
            user_profile.user.first_name = center_name
            user_profile.user.save()
            profile_form = form.save(commit=False)
            profile_form.user = request.user
            profile_form.save()
            try:
                user_profile.save()
            except Exception:
                return HttpResponse(
                    json.dumps(
                        {'status': False, 'message': 'Error Occures! Cannot update profile!'}
                    ),
                    content_type='application/json'
                )
            else:
                return HttpResponse(
                    json.dumps(
                        {'status': True, 'message': 'Profile Updated Successfully!'}
                    ),
                    content_type='application/json'
                )
        else:
            return HttpResponse(
                json.dumps(
                    {'status': False, 'message': 'Error Occures! Cannot update profile!'}
                ),
                content_type='application/json'
            )


# Update Details of Chief Functionary of a Center
@login_required
@user_passes_test(center_check)
def update_functionary(request):
    response = {}
    user_profile = UserProfile.objects.get(user=request.user)
    response.update({'user_profile': user_profile})
    if request.method == 'GET':
        try:
            functionary = ChiefFunctionary.objects.get(center=user_profile)
            response.update({'functionary': functionary})
            return render(request, 'functionary_update.html', response)
        except Exception:
            return render(request, 'functionary_update.html', response)
    if request.method == 'POST':
        user_profile = get_object_or_404(UserProfile, user=request.user)
        # Check whether functionary exists
        exists_func, created = ChiefFunctionary.objects.get_or_create(center=user_profile)
        if created:
            functionary_form = FunctionaryForm(request.POST)
        else:
            functionary_form = FunctionaryForm(request.POST, instance=exists_func)
        if functionary_form.is_valid():
            functionary = functionary_form.save(commit=False)
            functionary.center = user_profile
            try:
                functionary.save()
            except Exception:
                return HttpResponse(
                    json.dumps(
                        {'status': False, 'message': 'Error occures. Please try again!'}
                    ),
                    content_type='application/json'
                )
            else:
                return HttpResponse(
                    json.dumps(
                        {'status': True, 'message': 'Functionary details updated successfully!'}
                    ),
                    content_type='application/json'
                )
        else:
            return HttpResponse(
                json.dumps(
                    {'status': False, 'message': 'Error in updation! Please try agin!'}
                ),
                content_type='application/json'
            )


# Update Courses of a Center
@login_required
@user_passes_test(center_check)
def update_course(request):
    center = get_object_or_404(UserProfile, user=request.user)
    courses = dict(request.POST.iterlists())['course'] if 'course' in request.POST else []
    center.centercourse_set.all().delete()
    for course in courses:
        course_obj = get_object_or_404(Course, pk=course)
        center_course, created = CenterCourse.objects.get_or_create(center=center, course=course_obj)

    return HttpResponse(
        json.dumps(
            {'status': True, 'message': 'Course saved successfully!'}
        ),
        content_type='application/json'
    )


# List of courses of a center
@login_required
@user_passes_test(center_check)
def center_course_list(request):
    response = {}
    center = get_object_or_404(UserProfile, user=request.user)
    response.update({'center': center})
    return render(request, 'center_course_list.html', response)



