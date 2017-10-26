from django.conf.urls import include, url

import siteadmin.views

urlpatterns = [
    url(r'^dashboard/$', siteadmin.views.dashboard, name='dashboard'),
    url(r'^course/new/$', siteadmin.views.course_new, name='course_new'),
    url(r'^course/delete/$', siteadmin.views.course_delete, name='course_delete'),
    url(r'^course/$', siteadmin.views.course, name='course'),
    url(r'^ajax/courses/$', siteadmin.views.ajax_courses, name='ajax_courses'),
    url(r'^course/edit/$', siteadmin.views.course_edit, name='course_edit'),
    url(r'^course/subject/$', siteadmin.views.course_subject, name='course_subject'),
    url(r'^course/subject/new/$', siteadmin.views.course_subject_new, name='course_subject_new'),
    url(r'^message/list/$', siteadmin.views.siteadmin_message_list, name='siteadmin_messages_list'),
    url(r'^ajax/coursecode/$', siteadmin.views.siteadmin_ajax_coursecode, name='siteadmin_ajax_coursecode'),
    url(r'^course/category/$', siteadmin.views.course_category, name='course_category'),
    url(r'^course/category/delete/$', siteadmin.views.category_delete, name='category_delete'),
    url(r'^course/category/edit/$', siteadmin.views.category_edit, name='category_edit'),
    # Subjects
    url(r'^ajax/subjects/$', siteadmin.views.ajax_subjects, name='ajax_subjects'),
]