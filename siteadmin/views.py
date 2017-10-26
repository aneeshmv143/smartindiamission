# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.shortcuts import *
from django.template.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.core import serializers
from django.forms.models import model_to_dict


from main.models import UserProfile, ContactMessage
from course.models import Course, CourseCategory, CourseDuration, Subject

from smartmissionconfig.user_types import UserType

from siteadmin.forms import CourseForm, SubjectForm, CategoryForm


def admin_check(user):
    user_profile = get_object_or_404(UserProfile, user=user)
    return user_profile.user_type == UserType.types['Admin']


# Check course code exists
def siteadmin_ajax_coursecode(request):
    if 'course_code' in request.GET and request.GET['course_code']:
        course_code = request.GET['course_code']
    else:
        raise Http404
    try:
        Course.objects.get(code=course_code)
    except Exception:
        return HttpResponse(
            json.dumps(
                {'status': True, 'message': 'Course code available!'}
            ),
            content_type='application/json'
        )
    else:
        return HttpResponse(
            json.dumps(
                {'status': False, 'message': 'Course code already exists!'}
            ),
            content_type='application/json'
        )


@login_required
@user_passes_test(admin_check)
def dashboard(request):
    response = {}
    response.update({'user_profile': get_object_or_404(UserProfile, user=request.user)})
    response.update({'course': Course.objects.count()})
    return render_to_response('siteadmin_dashboard.html', response)


# Create new course form admin
@login_required
@user_passes_test(admin_check)
def course_new(request):
    response = {}
    response.update(csrf(request))
    user_profile = get_object_or_404(UserProfile, user=request.user)
    response.update({'user_profile': user_profile})
    if request.method == 'GET':
        response.update({'course_duration': CourseDuration.objects.all()})
        return render(request, 'siteadmin_course_new.html', response)
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            new_course = form.save(commit=False)
            new_course.is_active = True
            new_course.save()
            return HttpResponse(
                json.dumps(
                    {'status': True, 'message': 'Course Added Successfully!'}
                ),
                content_type='application/json'
            )
        else:
            return HttpResponse(
                json.dumps(
                    {'status': False, 'message': 'Error! Please Try Again!'}
                ),
                content_type='application/json'
            )


@login_required
@user_passes_test(admin_check)
def course(request):
    response = {}
    response.update({'user_profile': get_object_or_404(UserProfile, user=request.user)})
    response.update({'course_duration': CourseDuration.objects.all()})
    if request.method == 'GET':
        return render(request, 'siteadmin_course.html', response)
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            new_course = form.save(commit=False)
            new_course.is_active = True
            try:
                new_course.save()
            except Exception:
                return HttpResponse(
                    json.dumps(
                        {'status': False, 'message': 'Course cannot be saved!'}
                    )
                )
            else:
                course = Course.objects.last()
                data = {}
                data['status'] = True
                data['message'] = 'Course saved successfully!'
                data['course_name'] = course.name
                data['course_code'] = course.code
                data['duration'] = course.duration.duration
                return HttpResponse(
                    json.dumps(data),
                    content_type='application/json'
                )
        else:
            return HttpResponse(
                json.dumps(
                    {'status': False, 'message': 'Course cannot be saved!'}
                )
            )


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
            Course.objects.filter(category=course_category, is_active=True).order_by('id')
        )
    )


@login_required
@user_passes_test(admin_check)
def course_edit(request):
    response = {}
    response.update({'user_profile': get_object_or_404(UserProfile, user=request.user)})
    response.update(csrf(request))
    response.update({'course_duration': CourseDuration.objects.all()})
    if request.method == 'GET':
        if 'course' in request.GET and request.GET['course']:
            course_id = request.GET['course']
        else:
            raise Http404
        course = get_object_or_404(Course, pk=course_id)
        data = {}
        data['status'] = True
        data['category'] = course.category.title
        data['course_code'] = course.code
        data['course_name'] = course.name
        data['duration'] = course.duration.duration
        data['description'] = course.description
        data['course_id'] = course.pk
        return HttpResponse(
            json.dumps(data),
            content_type='application/json'
        )
    if request.method == 'POST':
        course_id = request.POST.get('course_id', '')
        course = get_object_or_404(Course, pk=course_id)
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            edit_course = form.save(commit=False)
            edit_course.is_active = True
            edit_course.save()
            data = {}
            data['status'] = True
            data['message'] = 'Course edited successfully!'
            data['code'] = edit_course.code
            data['name'] = edit_course.name
            data['duration'] = edit_course.duration.duration
            return HttpResponse(
                json.dumps(data),
                content_type='application/json'
            )
        else:
            return HttpResponse('Form Error')


# Delete a course
@login_required
@user_passes_test(admin_check)
def course_delete(request):
    if 'course' in request.GET and request.GET['course']:
        course = request.GET['course']
    else:
        raise Http404
    course_obj = get_object_or_404(Course, id=course)
    course_obj.is_active = False
    try:
        course_obj.save()
    except Exception:
        return HttpResponse(
            json.dumps(
                {'status': False, 'message': 'Course cannot de deleted!'}
            ),
            content_type='application/json'
        )
    else:
        return HttpResponse(
            json.dumps(
                {'status': True, 'message': 'Course deleted successfully!', 'course': course_obj.id}
            ),
            content_type='application/json'
        )


@login_required
@user_passes_test(admin_check)
def course_subject(request):
    return render(request, 'siteadmin_course_subject.html')


@login_required
@user_passes_test(admin_check)
def course_subject_new(request):
    response = {}
    response.update({'user_profile': get_object_or_404(UserProfile, user=request.user)})
    response.update(csrf(request))
    response.update({'course_categories': CourseCategory.objects.all()})

    if request.method == 'GET':
        response.update({'form': Subject()})
        return render_to_response('siteadmin_course_subject_new.html', response)

    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            response.update({'form': form})
            course = get_object_or_404(Course, pk=form.cleaned_data['course'])
            subject = Subject(course= course, subject_code= form.cleaned_data['subject_code'], subject_name= form.cleaned_data['subject_name'], description= form.cleaned_data['description'])
            try:
                subject.save()
            except Exception:
                response.update({'not_saved': True})
                return render_to_response('siteadmin_course_subject_new.html', response)
            else:
                return HttpResponse('Form Error')

        return HttpResponse(
            json.dumps({'msg': 'Subject Saved Successfully'}),
            content_type='application/json'
        )


@login_required
@user_passes_test(admin_check)
def siteadmin_message_list(request):
    response = {}
    response.update({'messages': ContactMessage.objects.all().order_by('-pk')[:20]})
    return render(request, 'siteadmin_messages.html', response)


# List & add course category
@login_required
@user_passes_test(admin_check)
def course_category(request):
    response = {}
    response.update(csrf(request))
    if request.method == 'GET':
        return render(request, 'siteadmin_course_category.html', response)
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            try:
                new_category = form.save(commit=False)
                new_category.is_active = True
                new_category.save()
            except Exception:
                return HttpResponse(
                    json.dumps(
                        {'status': False, 'message': 'Error found! Please try again!'}
                    ),
                    content_type='application/json'
                )
            else:
                category = CourseCategory.objects.last()
                data = {}
                data['status'] = True
                data['message'] = 'Course category added successfully!'
                data['category'] = category.title
                data['category_id'] = category.id
                return HttpResponse(
                    json.dumps(data),
                    content_type='application/json'
                )
        else:
            return HttpResponse(
                json.dumps(
                    {'status': False, 'message': 'Error found! Please try again!'}
                ),
                content_type='application/json'
            )


# Delete course category
@login_required
@user_passes_test(admin_check)
def category_delete(request):
    if 'category' in request.GET and request.GET['category']:
        category = request.GET['category']
    else:
        raise Http404
    category_obj = get_object_or_404(CourseCategory, id=category)
    category_obj.is_active = False
    try:
        category_obj.save()
    except Exception:
        return HttpResponse(
            json.dumps(
                {'status': False, 'message': 'Course category cannot delete!'}
            ),
            content_type='application/json'
        )
    else:
        return HttpResponse(
            json.dumps(
                {'status': True, 'message': 'Course category deleted successfully!', 'category': category_obj.id}
            ),
            content_type='application/json'
        )


# Edit course ctaegory
@login_required
@user_passes_test(admin_check)
def category_edit(request):
    if request.method == 'GET':
        if 'category' in request.GET and request.GET['category']:
            category = request.GET['category']
        else:
            raise Http404
        course_obj = get_object_or_404(CourseCategory, pk=category)
        data = {}
        data['status'] = True
        data['title'] = course_obj.title
        data['description'] = course_obj.description
        data['id'] = course_obj.pk
        return HttpResponse(
            json.dumps(data),
            content_type='application/json'
        )
    if request.method == 'POST':
        if 'category_id' in request.POST and request.POST['category_id']:
            category_id = request.POST['category_id']
            category = get_object_or_404(CourseCategory, pk=category_id)
        else:
            raise Http404
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            edit_category = form.save(commit=False)
            edit_category.is_active = True
            edit_category.save()
            data = {}
            data['status'] = True
            data['message'] = 'Category details updated successfully!'
            data['id'] = edit_category.pk
            data['title'] = edit_category.title
            return HttpResponse(
                json.dumps(data),
                content_type='application/json'
            )
        else:
            return HttpResponse('invalid form')


# Ajax subjects
@login_required
@user_passes_test(admin_check)
def ajax_subjects(request):
    if 'course' in request.GET and request.GET['course']:
        course_id = request.GET['course']
    else:
        raise Http404()
    course = get_object_or_404(Course, pk=course_id)
    return HttpResponse(
        serializers.serialize(
            'json',
            Subject.objects.filter(course=course, is_active=True).order_by('id')
        )
    )