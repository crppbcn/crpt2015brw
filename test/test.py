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
from crpt201511.constants import *
from crpt201511.utils.assessment_utils import get_remote_folder_name


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
    # new assessment - TODO: set generic procedure
    try:
        assessment = Assessment.objects.all()[:1].get()
    except:
        assessment = Assessment()
        assessment.name = "Test Assessment"
        assessment.city = City.objects.get(name="Test")
        assessment.considerations = "Test Assessment"
        assessment.focal_point_started = Person.objects.get(name="City, Test")
        assessment.version = AssessmentVersion.objects.order_by('-date_released')[0]
        assessment.save()

    # new City ID. For each section create AssessmentCityIDStatements and correspondent responses
    cid_sections = CityIDSection.objects.all()
    for section in cid_sections:
        print("CtyID Section Start: " + section.name)
        # CharField
        cid_questions = CityIDQuestionCharField.objects.filter(section=section)
        for cid_question in cid_questions:
            a_cid_question = AssessmentCityIDQuestionCharField()
            a_cid_question.question_short = cid_question.question_short
            a_cid_question.question_long = cid_question.question_long
            a_cid_question.order = cid_question.order
            a_cid_question.help_text = cid_question.help_text
            a_cid_question.placeholder = cid_question.placeholder
            a_cid_question.not_applicable = cid_question.not_applicable
            a_cid_question.version = cid_question.version
            a_cid_question.section = section
            a_cid_question.assessment = assessment
            a_cid_question.save()
        # TextField
        cid_questions = CityIDQuestionTextField.objects.filter(section=section)
        for cid_question in cid_questions:
            a_cid_question = AssessmentCityIDQuestionTextField()
            a_cid_question.question_short = cid_question.question_short
            a_cid_question.question_long = cid_question.question_long
            a_cid_question.order = cid_question.order
            a_cid_question.help_text = cid_question.help_text
            a_cid_question.placeholder = cid_question.placeholder
            a_cid_question.not_applicable = cid_question.not_applicable
            a_cid_question.version = cid_question.version
            a_cid_question.section = section
            a_cid_question.assessment = assessment
            a_cid_question.save()
        # SelectField
        cid_questions = CityIDQuestionSelectField.objects.filter(section=section)
        for cid_question in cid_questions:
            a_cid_question = AssessmentCityIDQuestionSelectField()
            a_cid_question.question_short = cid_question.question_short
            a_cid_question.question_long = cid_question.question_long
            a_cid_question.order = cid_question.order
            a_cid_question.help_text = cid_question.help_text
            a_cid_question.placeholder = cid_question.placeholder
            a_cid_question.not_applicable = cid_question.not_applicable
            a_cid_question.version = cid_question.version
            a_cid_question.section = section
            a_cid_question.assessment = assessment
            a_cid_question.choices = cid_question.choices
            a_cid_question.multi = cid_question.multi
            a_cid_question.save()

        # UploadField
        cid_questions = CityIDQuestionUploadField.objects.filter(section=section)
        for cid_question in cid_questions:
            a_cid_question = AssessmentCityIDQuestionUploadField()
            a_cid_question.question_short = cid_question.question_short
            a_cid_question.question_long = cid_question.question_long
            a_cid_question.order = cid_question.order
            a_cid_question.help_text = cid_question.help_text
            a_cid_question.placeholder = cid_question.placeholder
            a_cid_question.not_applicable = cid_question.not_applicable
            a_cid_question.version = cid_question.version
            a_cid_question.section = section
            a_cid_question.assessment = assessment
            a_cid_question.save()
        print("CityID Section End: " + section.name)
    print("test_create_new_assessment. End.")


def test_get_remote_folder_name():
    print("test_get_remote_folder_name.Start")

    assessment = Assessment.objects.all()[:1].get()
    section = CityIDSection.objects.all()[:1].get()

    print("remote folder name: " + get_remote_folder_name(assessment, section))


    print("test_get_remote_folder_name.End")


if __name__ == "__main__":
    #test_threading()
    #test_version_selected()
    #test_get_remote_folder_name()
    test_create_new_assessment()
