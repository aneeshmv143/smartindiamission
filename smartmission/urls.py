"""smartmission URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin

import main.views

admin.autodiscover()

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^$', main.views.index, name='index'),
    url(r'^about/$', main.views.about, name='about'),
    url(r'^objectives/$', main.views.objectives, name='objectives'),
    url(r'^workplan/$', main.views.workplan, name='workplan'),
    url(r'^course/list/(?P<pk>\w+)/$', main.views.course_list, name='course_list'),
    url(r'^course/details/(?P<pk>\w+)/$', main.views.course_details, name='course_details'),
    url(r'^contact/$', main.views.contact, name='contact'),
    url(r'^registration/$', main.views.registration, name='registration'),
    url(r'^login/$', main.views.login, name='login'),
    url(r'^logout/$', main.views.logout, name='logout'),
    url(r'^contact/message/$', main.views.contact_message, name='contact_message'),
    url(r'^register/$', main.views.register, name='register'),
    url(r'^account/activation/$', main.views.account_activation, name='account_activation'),
    url(r'^ajax/districts/$', main.views.ajax_districts, name='ajax_districts'),
    url(r'^ajax/courses/$', main.views.ajax_courses, name='ajax_courses'),

    url(r'^siteadmin/', include('siteadmin.urls', namespace='siteadmin')),
    url(r'^center/', include('center.urls', namespace='center')),

    url(r'^api/courses/', main.views.CourseListAPI.as_view(), name='list-course-api'),
]
