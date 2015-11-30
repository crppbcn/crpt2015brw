"""crpt201511 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # url admin app
    url(r'^admin/', include(admin.site.urls)),

    # url to form login
    url(r'^accounts/login/$', 'crpt201511.views.my_login', name="my_login"),

    # url to logout page
    url(r'^logout/$', 'crpt201511.views.my_logout', name='logout'),

    # url to change password
    url(r'^accounts/change_password/$', 'crpt201511.views.my_change_password', name='my_change_password'),

    # base url
    url(r'^$', 'crpt201511.views.welcome', name='welcome'),

    # url to my_copyright page
    url(r'^my_copyright/$', 'crpt201511.views.my_copyright', name='my_copyright'),

    # url to welcome page
    url(r'^welcome/$', 'crpt201511.views.welcome', name='welcome'),

    # url to steps page
    url(r'^steps/(?P<assessment_id>\d+)/$', 'crpt201511.views.steps', name='steps'),

    # url to city id form page
    url(r'^city_id/(?P<assessment_id>\d+)/(?P<element_id>\d+)/$', 'crpt201511.views.city_id', name='city_id'),
    url(r'^city_id/(?P<assessment_id>\d+)/$', 'crpt201511.views.city_id', name='city_id'),

]