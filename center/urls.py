from django.conf.urls import url

import center.views

urlpatterns = [
    url(r'^dashboard/$', center.views.dashboard, name='dashboard'),
    url(r'^profile/$', center.views.center_profile, name='center_profile'),
    url(r'^profile/update/$', center.views.update_center_profile, name='update_center_profile'),
    url(r'^functionary/update/$', center.views.update_functionary, name='update_functionary'),
    url(r'^course/update/$', center.views.update_course, name='update_course'),
    url(r'^course/list/$', center.views.center_course_list, name='center_course_list '),
    url(r'^ajax/course/$', center.views.center_ajax_course, name='center_ajax_course'),
]
