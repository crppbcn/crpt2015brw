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
import crpt201511.signals.receivers

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
    url(r'^welcome/(?P<assessment_id>\d+)/$', 'crpt201511.views.views.welcome', name='welcome'),
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

    url(r'^parent_component/(?P<assessment_id>\d+)/$', 'crpt201511.views.component_views.parent_component', name='parent_component'),
    url(r'^component_2/(?P<assessment_id>\d+)/(?P<component_id>\d+)/$', 'crpt201511.views.component_views.component_2', name='component_2'),
    url(r'^component_2/(?P<assessment_id>\d+)/(?P<component_id>\d+)/$', 'crpt201511.views.component_views.component_2', name='component_2'),
    url(r'^component_2/(?P<assessment_id>\d+)/(?P<component_id>\d+)/(?P<subcomponent_id>\d+)/$', 'crpt201511.views.component_views.component_2', name='component_2'),
    url(r'^component_2/(?P<assessment_id>\d+)/(?P<component_id>\d+)/(?P<subcomponent_id>\d+)/(?P<third_component_id>\d+)/$', 'crpt201511.views.component_views.component_2', name='component_2'),
    url(r'^component_2/(?P<assessment_id>\d+)/(?P<component_id>\d+)/(?P<subcomponent_id>\d+)/(?P<third_component_id>\d+)/(?P<fourth_component_id>\d+)/$', 'crpt201511.views.component_views.component_2', name='component_2'),
    url(r'^component_2/(?P<assessment_id>\d+)/(?P<component_id>\d+)/(?P<subcomponent_id>\d+)/(?P<third_component_id>\d+)/(?P<fourth_component_id>\d+)/(?P<fifth_component_id>\d+)/$', 'crpt201511.views.component_views.component_2', name='component_2'),
    # url to new question lgj
    url(r'^duplicate_question/(?P<assessment_id>\d+)/(?P<component_id>\d+)/(?P<subcomponent_id>\d+)/(?P<third_component_id>\d+)/(?P<initial_question_id>\d+)/$', 'crpt201511.views.component_views.duplicate_question', name='duplicate_question'),

    # hazards
    url(r'^hazard_groups/(?P<assessment_id>\d+)/$', 'crpt201511.views.hazard_views.hazard_groups', name='hazard_groups'),
    url(r'^hazard_types/(?P<assessment_id>\d+)/(?P<hg_id>\d+)/$', 'crpt201511.views.hazard_views.hazard_types', name='hazard_types'),
    url(r'^hazard_type_detail/(?P<assessment_id>\d+)/(?P<ht_id>\d+)/$', 'crpt201511.views.hazard_views.hazard_type_detail', name='hazard_type_detail'),
    url(r'^hazard_type_interrelations/(?P<assessment_id>\d+)/(?P<ht_id>\d+)/$', 'crpt201511.views.hazard_views.hazard_type_interrelations', name='hazard_type_interrelations'),
    url(r'^hazard_type_impacts/(?P<assessment_id>\d+)/(?P<ht_id>\d+)/(?P<element_id>\d+)/$', 'crpt201511.views.hazard_views.hazard_type_impacts', name='hazard_type_impacts'),
    url(r'^hazard_type_impacts/(?P<assessment_id>\d+)/(?P<ht_id>\d+)/$', 'crpt201511.views.hazard_views.hazard_type_impacts', name='hazard_type_impacts'),
    url(r'^hazards_selected/(?P<assessment_id>\d+)/$', 'crpt201511.views.hazard_views.hazards_selected', name='hazards_selected'),
    url(r'^hazards_relations/(?P<assessment_id>\d+)/$', 'crpt201511.views.hazard_views.hazards_relations', name='hazards_relations'),

    # stakeholders
    url(r'^stakeholder_groups/(?P<assessment_id>\d+)/$', 'crpt201511.views.stakeholder_views.stakeholder_groups', name='stakeholder_groups'),
    url(r'^stakeholders/(?P<assessment_id>\d+)/(?P<sg_id>\d+)/$', 'crpt201511.views.stakeholder_views.stakeholders', name='stakeholders'),
    url(r'^stakeholders/(?P<assessment_id>\d+)/(?P<sg_id>\d+)/(?P<st_id>\d+)/$', 'crpt201511.views.stakeholder_views.stakeholders', name='stakeholders'),
    url(r'^stakeholders/(?P<assessment_id>\d+)/(?P<sg_id>\d+)/(?P<st_id>\d+)/(?P<s_id>\d+)/$', 'crpt201511.views.stakeholder_views.stakeholders', name='stakeholders'),

    # url to test page
    url(r'^test/$', 'crpt201511.views.views.test', name='test'),
]
