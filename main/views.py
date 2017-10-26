# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import random
import string

from django.shortcuts import *
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.template.context_processors import csrf
from django.core.urlresolvers import reverse
from django.core.serializers import serialize
from django.core.mail import send_mail

from django.contrib.auth.models import User

from rest_framework import serializers, generics

from course.models import CourseCategory, Course, Subject
from main.models import UserProfile, ContactMessage, UserActivation
from static_data.models import State, District
from main.forms import RegisterForm

from smartmissionconfig.user_types import UserType


# Ajax Districts
def ajax_districts(request):
    if 'state' in request.GET and request.GET['state']:
        state_id = request.GET['state']
    else:
        raise Http404
    state = get_object_or_404(State, id=state_id)
    districts = District.objects.filter(state=state)
    return render(request, 'ajax_districts.html', {'districts': districts})


# Ajax Courses
def ajax_courses(request):
    if 'category' in request.GET and request.GET['category']:
        category_id = request.GET['category']
    else:
        raise Http404
    course_category = get_object_or_404(CourseCategory, id=category_id)
    courses = Course.objects.filter(category=course_category)
    return render(request, 'ajax_courses.html', {'courses': courses})


def index(request):
    response = {}
    response.update({'courses': Course.objects.all().count()})
    return render(request, 'index.html', response)


def about(request):
    return render(request, 'about.html')


def objectives(request):
    return render(request, 'objectives.html')


def workplan(request):
    return render(request, 'workplan.html')


def course_list(request, pk):
    response = {}
    category = get_object_or_404(CourseCategory, pk=pk)
    response.update({'category': category})
    response.update({'courses': Course.objects.filter(category=category)})
    return render(request, 'course_list.html', response)


def contact(request):
    return render(request, 'contact.html')


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
                auth_login(request, user)
                try:
                    user_profile = UserProfile.objects.get(user=user)
                except Exception:
                    raise Http404('No User Profile')
                if user_profile.user_type == UserType.types['Admin']:
                    return HttpResponseRedirect(reverse('siteadmin:dashboard'))
                if user_profile.user_type == UserType.types['Center']:
                    return HttpResponseRedirect(reverse('center:dashboard'))

            else:
                return HttpResponse('Inactive User')

        else:
            response.update({'invalid_login': True})
            return render(request, 'login.html', response)


# Logout user
def logout(request):
    response = {}
    response.update(csrf(request))
    auth_logout(request)
    # response.update({'logout':True})
    return HttpResponseRedirect('/')


# Course Details
def course_details(request, pk):
    response = {}
    response.update({'course_categories': CourseCategory.objects.all()})

    course = get_object_or_404(Course, pk=pk)
    response.update({'course': course})
    response.update({'course_details': CourseSubject.objects.filter(course=course)})
    return render_to_response('course_details.html', response)


# Contact Message
def contact_message(request):
    if request.method == 'GET':
        return render(request, 'contact.html')
    if request.method == 'POST':
        name = request.POST.get('name', '')
        contact_no = request.POST.get('contact_no', '')
        email = request.POST.get('email', '')
        message = request.POST.get('message', '')
        new_massage = ContactMessage(name=name, contact_no=contact_no, email=email, message=message)
        try:
            new_massage.save()
        except Exception:
            return HttpResponse(
                json.dumps(
                    {'status': False, 'message': 'Message could not send. Please try again!'}
                ),
                content_type='application/json'
            )
        else:
            return HttpResponse(
                json.dumps(
                    {'status': True, 'message': 'Message Send Successfully!'}
                ),
                content_type='application/json'
            )


def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                user = User.objects.get(email=email)
            except Exception:
                user = User(username=email, email=email, first_name=name, password=password)
                user.save()
                try:
                    # Create UserType in UserProfile
                    user_profile = UserProfile(user=user, user_type=UserType.types['Center'])
                    user_profile.save()
                except Exception:
                    pass
                else:
                    # Generate Key and Send to Email for activation
                    key = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(32))
                    activate_user = UserActivation(user=user, key=key)
                    activate_user.save()
                    send_mail(
                        'Smartindia Center Activation Link',
                        'Click on the link to activate your account ' + 'http://localhost:8000/account/activation/?user=' + str(user.id) + '&key=' + str(key) ,
                        'info@smartindiamission.org',
                        [user.email],
                        fail_silently=False
                    )
                    return render(request, 'register.html', {'user_registered': True})
            else:
                return render(request, 'register.html', {'user_exists': True})


# Activate Account
def account_activation(request):
    response = {}
    if 'user' in request.GET and request.GET['user']:
        user_id = request.GET['user']
    else:
        response.update({'invalid_access': True})
        return render(request, 'activated_link.html', response)
    if 'key' in request.GET and request.GET['key']:
        key = request.GET['key']
    else:
        response.update({'invalid_access': True})
        return render(request, 'activated_link.html', response)
    user = get_object_or_404(User, pk=user_id)
    try:
        valid_key = UserActivation.objects.get(user=user, key=key)
    except Exception:
        response.update({'invaid_access': True})
        return render(request, 'activated_link.html', response)
    else:
        valid_key.user.is_active = True
        valid_key.user.save()
        valid_key.delete()
    response.update({'valid_access': True})
    return render(request, 'activated_link.html', response)
    

class CourseListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class CourseListAPI(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseListSerializer
