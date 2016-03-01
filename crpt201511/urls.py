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
    url(r'^accounts/login/$', 'crpt201511.views.user_views.my_login', name="my_login"),

    # url to logout page
    url(r'^logout/$', 'crpt201511.views.user_views.my_logout', name='logout'),

    # url to change password
    url(r'^accounts/change_password/$', 'crpt201511.views.user_views.my_change_password', name='my_change_password'),

    # base url
    url(r'^$', 'crpt201511.views.views.welcome', name='welcome'),

    # url to my_copyright page
    url(r'^my_copyright/$', 'crpt201511.views.views.my_copyright', name='my_copyright'),

    # url to welcome page
    url(r'^welcome/$', 'crpt201511.views.views.welcome', name='welcome'),

    # url to steps page
    url(r'^steps/(?P<assessment_id>\d+)/$', 'crpt201511.views.views.steps', name='steps'),

    # url to city id form page
    url(r'^city_id/(?P<assessment_id>\d+)/(?P<section_id>\d+)/$', 'crpt201511.views.city_id_views.city_id', name='city_id'),
    url(r'^city_id/(?P<assessment_id>\d+)/(?P<section_id>\d+)/(?P<subsection_id>\d+)/$', 'crpt201511.views.city_id_views.city_id', name='city_id'),
    url(r'^city_id/(?P<assessment_id>\d+)/$', 'crpt201511.views.city_id_views.city_id', name='city_id'),

    # url to add comment to a section
    url(r'^add_section_comment/$', 'crpt201511.views.city_id_views.add_section_comment', name='add_section_comment'),

    # url to components form page
    url(r'^component/(?P<assessment_id>\d+)/(?P<component_id>\d+)/$', 'crpt201511.views.component_views.component', name='component'),
    url(r'^component/(?P<assessment_id>\d+)/(?P<component_id>\d+)/(?P<subcomponent_id>\d+)/$', 'crpt201511.views.component_views.component', name='component'),
    url(r'^component/(?P<assessment_id>\d+)/(?P<component_id>\d+)/(?P<subcomponent_id>\d+)/(?P<third_component_id>\d+)/$', 'crpt201511.views.component_views.component', name='component'),
    url(r'^component/(?P<assessment_id>\d+)/$', 'crpt201511.views.component_views.component', name='component'),

    # url to new question lgj
    url(r'^duplicate_question/(?P<assessment_id>\d+)/(?P<component_id>\d+)/(?P<subcomponent_id>\d+)/(?P<third_component_id>\d+)/(?P<initial_question_id>\d+)/(?P<question_type>[^/]+)/$', 'crpt201511.views.component_views.duplicate_question', name='duplicate_question'),

    # url to test page
    url(r'^test/$', 'crpt201511.views.views.test', name='test'),
]
