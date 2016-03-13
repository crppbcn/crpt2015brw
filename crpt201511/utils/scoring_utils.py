from __future__ import division

import sys

from crpt201511.models import *
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

        ret = float("{0:.2f}".format(total_score / scorable_questions_length))


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
    element.save()

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

        print("answered_noq: " + str(answered_noq))
        print("total_noq: " + str(total_noq))
        element.degree_of_completion = float("{0:.2f}".format(answered_noq * 100 / total_noq))
        element.save()
        print("degree_of_completion: " + str(element.degree_of_completion))


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
        # go for elements
        for elem in elements:
            organizational_score += float(elem.organizational_score)
            spatial_score += float(elem.spatial_score)
            physical_score += float(elem.physical_score)
            functional_score += float(elem.functional_score)
            degree_of_completion += float(elem.degree_of_completion)
        # final calculation
        element.organizational_score = float("{0:.2f}".format(organizational_score / elements_number))
        element.spatial_score = float("{0:.2f}".format(spatial_score / elements_number))
        element.physical_score = float("{0:.2f}".format(physical_score / elements_number))
        element.functional_score = float("{0:.2f}".format(functional_score / elements_number))
        element.degree_of_completion = float("{0:.2f}".format(degree_of_completion / elements_number))
        # save

        print("------------ aggregate_scoring_element ------------")
        print("Element: " + element.element.name)
        print("organizational_score: " + str(element.organizational_score))
        print("physical_score: " + str(element.physical_score))
        print("functional_score: " + str(element.functional_score))
        print("degree_of_completion: " + str(element.degree_of_completion))
        print("------------ aggregate_scoring_element ------------")


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
        # go for elements
        for elem in elements:
            organizational_score += float(elem.organizational_score)
            spatial_score += float(elem.spatial_score)
            physical_score += float(elem.physical_score)
            functional_score += float(elem.functional_score)
            degree_of_completion += float(elem.degree_of_completion)
        # Elements - final calculation
        assessment.organizational_score = float("{0:.2f}".format(organizational_score / elements_number))
        assessment.spatial_score = float("{0:.2f}".format(spatial_score / elements_number))
        assessment.physical_score = float("{0:.2f}".format(physical_score / elements_number))
        assessment.functional_score = float("{0:.2f}".format(functional_score / elements_number))

        # save assessment
        assessment.save()
    print("calculate_overall_assessment_scoring. End. " + str(assessment.id))
    sys.stdout.flush()



def calculate_city_id_completion(assessment):
    """
    Recalculates city id degree of copmpletion
    :param assessment:
    :return:
    """
    print("recalculate_city_id_completion.Start.")

    cidqs_total = len(AssessmentCityIDQuestion.objects.filter(assessment=assessment))
    cidqs_answered = 0
    for cidq in AssessmentCityIDQuestion.objects.filter(assessment=assessment):
        if str(cidq.response).strip() != "":
            cidqs_answered += 1

    assessment.city_id_completion = float("{0:.2f}".format(cidqs_answered * 100 / cidqs_total))
    assessment.save()

    print("recalculate_city_id_completion.End.")


def calculate_hazards_completion(assessment):
    """
    Recalculate hazards completion
    :param assessment:
    :return:
    """
    print("recalculate_hazards_completion.Start.")

    ahts = AssessmentHazardType.objects.filter(assessment=assessment, risk_assessment__in=["1","2"])
    ahts_total = len(ahts)
    ahts_answered_ok = 0
    for aht in ahts:
        hs_answered = len(AssessmentHazardSubtype.objects.filter(assessment=assessment, a_h_type=aht, enabled=True)) > 0
        h_causes = len(AssessmentHazardCause.objects.filter(assessment=assessment, a_h_type=aht, enabled=True)) > 0
        h_conseq = len(AssessmentHazardConsequence.objects.filter(assessment=assessment, a_h_type=aht, enabled=True)) > 0
        if hs_answered and h_causes and h_conseq:
            ahts_answered_ok += 1
    assessment.hazards_completion = float("{0:.2f}".format(ahts_answered_ok / ahts_total * 100))
    assessment.save()

    print("recalculate_hazards_completion.End.")


def calculate_stakeholders_completion(assessment):
    """
    Recalculates stakeholders completion
    :param assessment:
    :return:
    """
    print("recalculate_stakeholders_completion.Start.")

    total = len(AssessmentStakeholder.objects.all())
    answered = len(AssessmentStakeholder.objects.filter(assessment=assessment, engagement_from_local_gov__in=["1","2","3"]))
    assessment.stakeholders_completion = float("{0:.2f}".format(answered / total * 100))
    assessment.save()

    print("recalculate_stakeholders_completion.End.")


def calculate_mov(assessment):
    assessment.mov_public_knowledge_noq = \
        len(AssessmentComponentQuestion.objects.filter(assessment=assessment, choices=MOV_SOURCE, response="1"))
    assessment.mov_media_noq = \
        len(AssessmentComponentQuestion.objects.filter(assessment=assessment, choices=MOV_SOURCE, response="2"))
    assessment.mov_official_document_noq = \
        len(AssessmentComponentQuestion.objects.filter(assessment=assessment, choices=MOV_SOURCE, response="3"))
    assessment.save()


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
    # save
    element.save()

    print("------------ Overall element scoring ------------")
    print("Element: " + element.element.name)
    print("organizational_score: " + str(element.organizational_score))
    print("physical_score: " + str(element.physical_score))
    print("functional_score: " + str(element.functional_score))
    print("degree_of_completion: " + str(element.degree_of_completion))
    print("------------ Overall element scoring ------------")


    # throw overall calculation of parent elements
    calculate_overall_parent_element(element)
    # throw overall calculation for assessment
    calculate_overall_assessment_scoring(element.assessment)
    # calculate degree of completion for each section
    calculate_degree_of_completion(element)
    calculate_city_id_completion(element.assessment)
    calculate_hazards_completion(element.assessment)
    calculate_stakeholders_completion(element.assessment)
    # calculate mov
    calculate_mov(element.assessment)

    print("calculate_overall_element_scoring. End. " + str(element.id))
    sys.stdout.flush()


def calculate_overall_assessment_scoring2(assessment):
    # organizational
    dimension = Dimension.objects.get(name=ORGANIZATIONAL)
    questions_org = AssessmentComponentQuestion.objects.filter(assessment=assessment, dimension=dimension, scorable=True).exclude(units=2)
    noq_org = len(questions_org)
    score_org = 0
    for q in questions_org:
        score_org += q.score
    print("Organizational Dimension:")
    print("noq: " + str(noq_org))
    print("score qs" + str(score_org))
    print("score dimension: " + str(float("{0:.2f}".format(score_org / noq_org))))

    assessment.organizational_score = float("{0:.2f}".format(score_org / noq_org))

    # functional
    dimension = Dimension.objects.get(name=FUNCTIONAL)
    questions_org = AssessmentComponentQuestion.objects.filter(assessment=assessment, dimension=dimension, scorable=True).exclude(units=2)
    noq_org = len(questions_org)
    score_org = 0
    for q in questions_org:
        score_org += q.score
    assessment.functional_score = float("{0:.2f}".format(score_org / noq_org))
    print("Functional Dimension:")
    print("noq: " + str(noq_org))
    print("score qs" + str(score_org))
    print("score dimension: " + str(float("{0:.2f}".format(score_org / noq_org))))

    # Physical
    dimension = Dimension.objects.get(name=PHYSICAL)
    questions_org = AssessmentComponentQuestion.objects.filter(assessment=assessment, dimension=dimension, scorable=True).exclude(units=2)
    noq_org = len(questions_org)
    score_org = 0
    for q in questions_org:
        score_org += q.score
    print("Physical Dimension:")
    print("noq: " + str(noq_org))
    print("score qs" + str(score_org))
    print("score dimension: " + str(float("{0:.2f}".format(score_org / noq_org))))
    assessment.physical_score = float("{0:.2f}".format(score_org / noq_org))
    # save
    assessment.save()
