"""Mitarbet URL Configuration

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
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from authentication import views
from projects import views as projects_views
from django.contrib import admin




urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout,{'next_page':'/login'}, name='logout'),
    url(r'^register/$', views.register, name='register'),
    url(r'^profile/(?P<username>[a-zA-Z0-9]+)/$', views.profile, name='profile'),
    url(r'^projects/$', projects_views.index, name='projects'),
    url(r'^projects/new/$', projects_views.add_project, name='add_project'),
    url(r'^projects/(?P<project_id>[0-9]+)/$', projects_views.project, name='project'),
    url(r'^projects/(?P<project_id>[0-9]+)/edit/$', projects_views.edit_project, name='edit_project'),
    url(r'^projects/(?P<project_id>[0-9]+)/edit/wiki$', projects_views.edit_project, name='wiki'),
    url(r'^projects/(?P<project_id>[0-9]+)/developers/$', projects_views.add_developer, name='add_developer'),
    url(r'^projects/(?P<project_id>[0-9]+)/discussions/$', projects_views.discussion_list, name='discussion_list'),
    url(r'^projects/(?P<project_id>[0-9]+)/discussions/new/$', projects_views.add_discussion, name='add_discussion'),
    url(r'^projects/(?P<project_id>[0-9]+)/discussions/(?P<discussion_id>[0-9]+)/$', projects_views.discussion, name='discussion'),
    url(r'^projects/(?P<project_id>[0-9]+)/discussions/(?P<discussion_id>[0-9]+)/comment/$', projects_views.comment, name='comment'),
]
