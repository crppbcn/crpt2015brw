from __future__ import division

import sys

from crpt201511.models import AssessmentComponentQuestion, Dimension, AssessmentElement, AssessmentCityIDQuestion
from crpt201511.constants import *


def calculate_dimension_element_scoring(element, dimension):
    """
    Calculation of scoring for each dimension
    :param element:
    :param dimension:
    :return:
    """
    print("calculate_dimension_element_scoring. Start. " + str(element.id) + " -  Dimension: " + dimension.name)
    scorable_questions = AssessmentComponentQuestion.objects.filter(assessment_element=element, scorable=True,
                                                                    dimension=dimension).exclude(mov_position__gt=-1).order_by('id')
    scorable_questions_length = len(scorable_questions)
    ret = 0

    if scorable_questions_length > 0:
        total_score = 0
        for question in scorable_questions:
            print("score: " + str(question.score))
            total_score += float(question.score)

        ret = total_score / scorable_questions_length

    print("calculate_dimension_element_scoring. End. " + str(element.id) + " -  Dimension: " + dimension.name)
    sys.stdout.flush()

    return ret


def calculate_degree_of_certainty(element):
    """
    calculation of MoV degree of certainty
    :param element:
    :return:
    """
    print("calculate_degree_of_certainty. Start. " + str(element.id))
    questions = AssessmentComponentQuestion.objects.filter(assessment_element=element, choices=MOV_SOURCE)

    # reset counters in element
    element.mov_public_knowledge_noq = 0
    element.mov_media_noq = 0
    element.mov_official_document_noq = 0

    for q in questions:
        if q.score == 1:
            element.mov_public_knowledge_noq += 1
        if q.score == 2:
            element.mov_media_noq += 1
        if q.score == 3:
            element.mov_official_document_noq += 1
    print("calculate_degree_of_certainty. End. " + str(element.id))
    sys.stdout.flush()


def calculate_degree_of_completion(element):
    """
    Calculation of the degree of completion
    :param element:
    :return:
    """
    print("calculate_degree_of_completion. Start. " + str(element.id))
    # get questions
    questions = AssessmentComponentQuestion.objects.filter(assessment_element=element, scorable=True).\
        exclude(mov_position__gt=-1)
    # calculate total noq
    total_noq = len(questions)
    # reset element previous calculation
    element.degree_of_completion = 0
    # recalculate noq answered questions
    if total_noq > 0:
        answered_noq = 0
        for q in questions:
            if q.response and str(q.response) != "":
                answered_noq += 1

        element.degree_of_completion = answered_noq / total_noq

    print("calculate_degree_of_completion. End. " + str(element.id))
    sys.stdout.flush()


def aggregate_scoring_element(element):
    """
    Aggregation of results for elements without questions
    :param element:
    :return:
    """
    print("aggregate_scoring_element. Start. " + str(element.id))
    # initialization
    elements = AssessmentElement.objects.filter(parent=element)
    elements_number = len(elements)
    print("aggregate_scoring_element. elements_number: " + str(elements_number))
    if elements_number > 0:
        # initialization of counters
        organizational_score = 0
        spatial_score = 0
        physical_score = 0
        functional_score = 0
        degree_of_completion = 0
        element.mov_public_knowledge_noq = 0
        element.mov_media_noq = 0
        element.mov_official_document_noq = 0
        # go for elements
        for elem in elements:
            organizational_score += float(elem.organizational_score)
            spatial_score += float(elem.spatial_score)
            physical_score += float(elem.physical_score)
            functional_score += float(elem.functional_score)
            element.mov_public_knowledge_noq += int(elem.mov_public_knowledge_noq)
            element.mov_media_noq += int(elem.mov_media_noq)
            element.mov_official_document_noq += int(elem.mov_official_document_noq)
            degree_of_completion += float(elem.degree_of_completion)
        # final calculation
        element.organizational_score = organizational_score / elements_number
        element.spatial_score = spatial_score / elements_number
        element.physical_score = physical_score / elements_number
        element.functional_score = functional_score / elements_number
        element.degree_of_completion = degree_of_completion / elements_number
        # save
        element.save()
    # return parent to continue recursively
    print("aggregate_scoring_element. End. " + str(element.id))
    sys.stdout.flush()

    return element.parent


def calculate_overall_parent_element(element):
    """
    Recursive calculation of parent elements
    :param element:
    :return:
    """
    print("calculate_overall_parent_element. Start. " + str(element.id))
    parent = element.parent
    while parent:
        parent = aggregate_scoring_element(parent)
    print("calculate_overall_parent_element. End. " + str(element.id))
    sys.stdout.flush()


def calculate_overall_assessment_scoring(assessment):
    """
    Calculation of assessment scoring, degree of certainty and degree of completion
    :param assessment:
    :return:
    """
    print("calculate_overall_assessment_scoring. Start. " + str(assessment.id))
    # Elements calculation  - initialization
    elements = AssessmentElement.objects.filter(assessment=assessment, parent=None).order_by('id')
    elements_number = len(elements)
    if elements_number > 0:
        organizational_score = 0
        spatial_score = 0
        physical_score = 0
        functional_score = 0
        degree_of_completion = 0
        assessment.mov_public_knowledge_noq = 0
        assessment.mov_media_noq = 0
        assessment.mov_official_document_noq = 0
        # go for elements
        for elem in elements:
            organizational_score += float(elem.organizational_score)
            spatial_score += float(elem.spatial_score)
            physical_score += float(elem.physical_score)
            functional_score += float(elem.functional_score)
            assessment.mov_public_knowledge_noq += int(elem.mov_public_knowledge_noq)
            assessment.mov_media_noq += int(elem.mov_media_noq)
            assessment.mov_official_document_noq += int(elem.mov_official_document_noq)
            degree_of_completion += float(elem.degree_of_completion)
        # Elements - final calculation
        assessment.organizational_score = organizational_score / elements_number
        assessment.spatial_score = spatial_score / elements_number
        assessment.physical_score = physical_score / elements_number
        assessment.functional_score = functional_score / elements_number
        assessment.degree_of_completion = degree_of_completion / elements_number
        # City ID - calculation
        assessment.city_id_completion = 0
        cid_questions = AssessmentCityIDQuestion.objects.filter(assessment=assessment).\
            exclude(question_type=UPLOAD_FIELD)
        total_noq = len(cid_questions)
        noq_answered = 0
        for question in cid_questions:
            if question.response and str(question.response).strip() != "":
                noq_answered += 1
        assessment.city_id_completion = noq_answered / total_noq
        # save assessment
        assessment.save()
    print("calculate_overall_assessment_scoring. End. " + str(assessment.id))
    sys.stdout.flush()


def calculate_overall_element_scoring(element):
    """
    Calculation of element scoring, degree of certainty and degree of completion
    :param element:
    :return:
    """
    print("calculate_overall_element_scoring. Start. " + str(element.id) + "-" + element.element.name)

    # first scoring for scorable questions and dimensions
    dimension = Dimension.objects.get(name=ORGANIZATIONAL)
    element.organizational_score = calculate_dimension_element_scoring(element, dimension)
    dimension = Dimension.objects.get(name=SPATIAL)
    element.spatial_score = calculate_dimension_element_scoring(element, dimension)
    dimension = Dimension.objects.get(name=PHYSICAL)
    element.physical_score = calculate_dimension_element_scoring(element, dimension)
    dimension = Dimension.objects.get(name=FUNCTIONAL)
    element.functional_score = calculate_dimension_element_scoring(element, dimension)
    # calculation of MoV degree of certainty
    calculate_degree_of_certainty(element)
    # calculation of degree of completion
    calculate_degree_of_completion(element)
    # save
    element.save()
    # throw overall calculation of parent elements
    calculate_overall_parent_element(element)
    # throw overall calculation for assessment
    calculate_overall_assessment_scoring(element.assessment)
    print("calculate_overall_element_scoring. End. " + str(element.id))
    sys.stdout.flush()