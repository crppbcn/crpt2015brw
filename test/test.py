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


def test_create_new_assessment_city_id():
    print("create_new_asessment_city_id. Start.")
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
            # creation of other tx choices for this assessment
            if cid_question.choices.strip() == OTHER_TX:
                for other_tx in ChoicesOtherTx.objects.all():
                    a_cid_other_tx = AssessmentCityIDChoicesOtherTx()
                    a_cid_other_tx.name = other_tx
                    a_cid_other_tx.assessment = assessment
                    a_cid_other_tx.save()
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
    print("create_new_asessment_city_id. End.")


def test_create_new_assessment_components():
    print("test_create_new_assessment_components. Start.")
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

    # Components (indicators). For each component create AssessmentQuestions and correspondent responses
    components = Component.objects.all()
    for component in components:
        print("Component Start: " + component.name)
        # CharField
        component_questions = ComponentQuestionCharField.objects.filter(component=component)
        for question in component_questions:
            a_question = AssessmentComponentQuestionCharField()
            a_question.question_short = question.question_short
            a_question.question_long = question.question_long
            a_question.order = question.order
            a_question.help_text = question.help_text
            a_question.placeholder = question.placeholder
            a_question.not_applicable = question.not_applicable
            a_question.version = question.version
            a_question.component = component
            a_question.assessment = assessment
            a_question.has_mov = question.has_mov
            a_question.units = question.units
            a_question.mov_position = question.mov_position
            a_question.save()
        # TextField
        component_questions = ComponentQuestionTextField.objects.filter(component=component)
        for question in component_questions:
            a_question = AssessmentComponentQuestionCharField()
            a_question.question_short = question.question_short
            a_question.question_long = question.question_long
            a_question.order = question.order
            a_question.help_text = question.help_text
            a_question.placeholder = question.placeholder
            a_question.not_applicable = question.not_applicable
            a_question.version = question.version
            a_question.component = component
            a_question.assessment = assessment
            a_question.has_mov = question.has_mov
            a_question.mov_position = question.mov_position
            a_question.units = question.units
            a_question.save()
            # SelectField
        component_questions = ComponentQuestionSelectField.objects.filter(component=component)
        for question in component_questions:
            a_question = AssessmentComponentQuestionSelectField()
            a_question.question_short = question.question_short
            a_question.question_long = question.question_long
            a_question.order = question.order
            a_question.help_text = question.help_text
            a_question.placeholder = question.placeholder
            a_question.not_applicable = question.not_applicable
            a_question.version = question.version
            a_question.component = component
            a_question.assessment = assessment
            a_question.choices = question.choices
            a_question.multi = question.multi
            a_question.has_mov = question.has_mov
            a_question.units = question.units
            a_question.mov_position = question.mov_position
            a_question.save()
            # creation of other tx choices for this assessment
            if question.choices.strip() == MC1:
                for other_tx in ChoicesOtherTx.objects.all():
                    a_cid_other_tx = AssessmentChoicesMC1()
                    a_cid_other_tx.name = other_tx
                    a_cid_other_tx.assessment = assessment
                    a_cid_other_tx.save()
        print("Component End: " + component.name)

    print("test_create_new_assessment_components. End.")


def test_get_remote_folder_name():
    print("test_get_remote_folder_name.Start")

    assessment = Assessment.objects.all()[:1].get()
    section = CityIDSection.objects.all()[:1].get()

    print("remote folder name: " + get_remote_folder_name(assessment, section))


    print("test_get_remote_folder_name.End")


def test_multi():
    print("test_multi.Start")
    question = AssessmentCityIDQuestionSelectField.objects.get(id=14)
    print("QUESTION: " + question.question_short)
    print("MULTI: " + str(question.multi))
    print("test_multi.End")


def test_simple():
    print("value: " + str(int("YES" == YES_STR)))
    print("value: " + str(int("" == YES_STR)))

if __name__ == "__main__":
    #test_threading()
    #test_version_selected()
    #test_get_remote_folder_name()
    #test_multi()
    #test_simple()
    test_create_new_assessment_city_id()
    test_create_new_assessment_components()



