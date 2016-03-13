from __future__ import division

import os,sys

from django.conf import settings

project_path = "/Users/miquel/UN/0003-CRPTDEV/CRPT201511/"
sys.path.append(project_path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'crpt201511.settings'

# OBS: to initialize Django in 1.7 and run python scripts. Do not include 'setup' in installed_apps
import django
django.setup()


from crpt201511.models import *
from crpt201511.constants import MOV_SOURCE
from crpt201511.utils.scoring_utils import *


def create_data_elements(assessment):
    """
    Creates data for element questions
    :return:
    """
    print("create_data_elements.Start.")

    # elements
    questions = AssessmentComponentQuestion.objects.filter(assessment=assessment, scorable=True).exclude(units=2).order_by('id')
    for q in questions:
        # div by 2 - low values
        if q.units == 1:
            q.response = "56.9"
        if q.choices_length > 0:
            if q.question_type == SELECT_SINGLE:
                q.response = str(1)
            if q.question_type == SELECT_MULTI:
                q.response = "u'" + str(q.choices_length-1) + "'"

        # div by 3
        if q.id % 3 == 0:
            if q.units == 1:
                q.response = "60.4"
            if q.choices_length > 0:
                if q.question_type == SELECT_SINGLE:
                    q.response = str(q.choices_length-1)
                if q.question_type == SELECT_MULTI:
                    q.response = "u'" + str(q.choices_length-1) + "'"
        # div by 5
        if q.id % 5 == 0:
            if q.units == 1:
                q.response = "79.8"
            if q.choices_length > 0:
                if q.question_type == SELECT_SINGLE:
                    q.response = str(q.choices_length -1)
                if q.question_type == SELECT_MULTI:
                    q.response = "u'" + str(q.choices_length-1) + "'"
        # div by 7
        if q.id % 7 == 0:
            if q.units == 1:
                q.response = "85.5"
            if q.choices_length > 0:
                if q.question_type == SELECT_SINGLE:
                    q.response = str(q.choices_length -1)
                if q.question_type == SELECT_MULTI:
                    q.response = "u'" + str(q.choices_lengt -1) + "'"
        # div by 9
        if q.id % 9 == 0:
            if q.units == 1:
                q.response = "91.1"
            if q.choices_length > 0:
                if q.question_type == SELECT_SINGLE:
                    q.response = str(q.choices_length -1)
                if q.question_type == SELECT_MULTI:
                    q.response = "u'" + str(q.choices_length -1) + "'"
        # div by 11
        if q.id % 11 == 0:
            if q.units == 1:
                q.response = "97.9"
            if q.choices_length > 0:
                if q.question_type == SELECT_SINGLE:
                    q.response = str(q.choices_length-1)
                if q.question_type == SELECT_MULTI:
                    q.response = "u'" + str(q.choices_length-1) + "'"

        # MoV
        if q.choices == MOV_SOURCE:
            if q.id % 2 == 0:
                q.response = "1"
            if q.id % 3 == 0:
                q.response = "2"
            if q.id % 5 == 0:
                q.response = "3"

        # save data
        q.save()

    print("create_data_elements.End.")


def create_data_city_id(assessment):
    """
    Creates data for city ID
    :param assessment:
    :return:
    """
    print("create_data_city_id.Start.")

    questions = AssessmentCityIDQuestion.objects.filter(assessment=assessment, question_type=CHAR_FIELD)
    for q in questions:
        q.response = "Test Data"
        q.save()

    print("create_data_city_id.End.")


def create_data_hazards(assessment):
    """
    Creates data for hazards
    :param assessment:
    :return:
    """
    print("create_data_hazards.Start.")
    # hazard types
    for aht in AssessmentHazardType.objects.filter(assessment=assessment).order_by('id'):
        if aht.id % 3 == 0:
            aht.risk_assessment = "2"
            aht.contingency_plan = "1"
            for ahts in AssessmentHazardSubtype.objects.filter(a_h_type=aht, assessment=assessment).order_by('id'):
                if ahts.id % 5 == 0:
                    ahts.enabled = True
                    ahts.save()
            for ahts in AssessmentHazardCause.objects.filter(a_h_type=aht, assessment=assessment).order_by('id'):
                if ahts.id % 5 == 0:
                    ahts.enabled = True
                    ahts.save()
            for ahts in AssessmentHazardConsequence.objects.filter(a_h_type=aht, assessment=assessment).order_by('id'):
                if ahts.id % 5 == 0:
                    ahts.enabled = True
                    ahts.save()
            for ahts in AssessmentElementImpact.objects.filter(a_h_type=aht, assessment=assessment).order_by('id'):
                if ahts.id % 5 == 0:
                    ahts.enabled = True
                    ahts.save()
            aht.save()
    print("create_data_hazards.End.")


def create_data_stakeholders(assessment):
    """
    Creates data for stakeholders
    :param assessment:
    :return:
    """
    print("create_data_stakeholders.Start.")

    for s in AssessmentStakeholder.objects.filter(assessment=assessment).order_by('id'):
        if s.id % 3 == 0:
            s.engagement_from_local_gov == "1"
        if s.id % 5 == 0:
            s.engagement_from_local_gov == "2"
        if s.id % 7 == 0:
            s.engagement_from_local_gov == "3"
        s.save()

    print("create_data_stakeholders.End.")


def get_assessment_element_children(assessment_element):
    return AssessmentElement.objects.filter(parent=assessment_element)



if __name__ == "__main__":
    assessment = Assessment.objects.all()[:1].get()

    create_data_elements(assessment)
    create_data_city_id(assessment)
    #create_data_hazards(assessment)
    #create_data_stakeholders(assessment)
    #recalculate_scoring(assessment)  # includes recalculation of completion for each section
    calculate_city_id_completion(assessment)
    calculate_overall_assessment_scoring2(assessment)
