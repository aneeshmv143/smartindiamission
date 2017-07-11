from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required
import siteadmin.views

urlpatterns = [
    url(r'^dashboard/$', siteadmin.views.dashboard, name='dashboard'),
    url(r'^course/list/$', siteadmin.views.course_list, name='course_list'),
    url(r'^ajax/courses/$', siteadmin.views.ajax_courses, name='ajax_courses'),
    url(r'^course/edit/$', siteadmin.views.course_edit, name='course_edit'),
   
]