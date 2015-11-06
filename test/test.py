import os
import sys

from threading import Thread

from django.conf import settings

project_path = "/Users/miquel/UN/0003-CRPTDEV/CRPT201511/"
sys.path.append(project_path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'crpt201511.settings'

# OBS: to initialize Django in 1.7 and run python scripts. Do not include 'setup' in installed_apps
import django
django.setup()

from crpt201511.trace import trace_action
from crpt201511.models import *
from crpt201511.constants import TRACE_LOGIN


def test_threading():
    print("test_threading. Start.")
    person = Person.objects.get(first_name="Test")
    t = Thread(target=trace_action, args=(TRACE_LOGIN, person, person.name + " - " + person.role.name))
    t.start()
    print("test_threading. End.")


def test_version_selected():
    print("test_version_selected. Start.")
    version = AssessmentVersion.objects.order_by('-date_released')[0]
    print("Version: " + version.version)
    print("test_version_selected. End.")


def test_create_new_assessment():
    print("test_create_new_assessment. Start.")
    # new assessment
    assessment = Assessment()
    assessment.name = "Test Assessment"
    assessment.city = City.objects.get(name="Test")
    assessment.considerations = "Test Assessment"
    assessment.focal_point_started = Person.objects.get(name="City, Test")
    assessment.version = AssessmentVersion.objects.order_by('-date_released')[0]
    assessment.save()
    # new City ID
    cid_sections = CityIDSection.objects.all()
    for section in cid_sections:
        cid_statements = CityIDCharFieldStatement.objects.filter(section=section)
        for statement in cid_statements:
            question = AssessmentCityIDCharFieldQuestion()
            question.assessment = assessment
            question.statement = statement
            question.save()
        cid_statements = CityIDTextFieldStatement.objects.filter(section=section)
        for statement in cid_statements:
            question = AssessmentCityIDTextFieldQuestion()
            question.assessment = assessment
            question.statement = statement
            question.save()


    # new elements questions


    print("test_create_new_assessment. End.")


if __name__ == "__main__":
    #test_threading()
    #test_version_selected()
    test_create_new_assessment()

