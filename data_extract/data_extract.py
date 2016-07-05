# from __future__ import unicode_literals

# encoding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import csv
import os



from django.conf import settings

project_path = "/Users/miquel/UN/0003-CRPTDEV/CRPT201511_BRW/"
sys.path.append(project_path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'crpt201511.settings'


# OBS: to initialize Django in 1.7 and run python scripts. Do not include 'setup' in installed_apps
import django
django.setup()

from django.contrib.auth.models import User, Group
from crpt201511.models import *


def get_new_response(choices, response):
    new_response = ""
    # get ids
    choices_ids = get_list_of_ids(response)
    # get values
    if choices == CITY_ROLE:
        for id in choices_ids:
            new_response += ChoicesCityRole.objects.get(id=id).name + ","
    if choices == ChoicesAirTx:
        for id in choices_ids:
            new_response += ChoicesAirTx.objects.get(id=id).name + ","
    if choices == ChoicesStakeholders:
        for id in choices_ids:
            new_response += ChoicesStakeholders.objects.get(id=id).name + ","
    if choices == ChoicesGasSupply:
        for id in choices_ids:
            new_response += ChoicesGasSupply.objects.get(id=id).name + ","
    if choices == ChoicesRailTx:
        for id in choices_ids:
            new_response += ChoicesRailTx.objects.get(id=id).name + ","
    if choices == ChoicesMC1:
        for id in choices_ids:
            new_response += ChoicesMC1.objects.get(id=id).name + ","
    if choices == ChoicesMC2:
        for id in choices_ids:
            new_response += ChoicesMC2.objects.get(id=id).name + ","
    if choices == ChoicesSC1:
        for id in choices_ids:
            new_response += ChoicesSC1.objects.get(id=id).name + ","
    if choices == ChoicesSC2:
        for id in choices_ids:
            new_response += ChoicesSC2.objects.get(id=id).name + ","
    if choices == ChoicesSC3:
        for id in choices_ids:
            new_response += ChoicesSC3.objects.get(id=id).name + ","
    if choices == ChoicesSC4:
        for id in choices_ids:
            new_response += ChoicesSC4.objects.get(id=id).name + ","
    if choices == ChoicesSC5:
        for id in choices_ids:
            new_response += ChoicesSC5.objects.get(id=id).name + ","
    if choices == ChoicesSC6:
        for id in choices_ids:
            new_response += ChoicesSC6.objects.get(id=id).name + ","
    if choices == ChoicesSC7:
        for id in choices_ids:
            new_response += ChoicesSC7.objects.get(id=id).name + ","
    return new_response


def extract_city_id_assessment(assessment_id, city_name):
    print("extract_city_id_assessment.Start. assessment_id: " + str(assessment_id))
    # open file
    file_path = settings.BASE_DIR + "/extract/"  + str(city_name) + "-CityIDQuestions.csv"
    with open(file_path, 'w') as f:
        writer = csv.writer(f, delimiter='|', lineterminator='\n')

        # load City ID questions
        city_id_sections = CityIDSection.objects.all().order_by('code')
        for section in city_id_sections:
            city_id_questions = AssessmentCityIDQuestion.objects.filter(assessment_id=assessment_id, section=section).\
            order_by('section_id','id')
            # write City ID questions
            for q in city_id_questions:
                parent_chain = []
                parent_names = ""
                parent = q.section.parent
                while parent:
                    parent_chain.append(parent.name)
                    parent = parent.parent
                for name in reversed(parent_chain):
                    parent_names += name + " - "

                if q.choices and str(q.choices).strip() != "":
                    q.response = get_new_response(q.choices, q.response)
                if not q.response:
                    q.response = ""

                row = [str(parent_names),
                       str(q.section.name),
                       str(q.question_long),
                       str(q.response)]
                writer.writerow(row)

    # close file
    f.close()

    print("extract_city_id_assessment.Start. assessment_id: " + str(assessment_id))


def extract_stakeholders_assessment(assessment_id, city_name):
    print("extract_stakeholders_assessment.Start. assessment_id: " + str(assessment_id))
    # open file
    file_path = settings.BASE_DIR + "/extract/" + str(city_name) + "-StakeholderQuestions.csv"
    with open(file_path, 'w') as f:
        writer = csv.writer(f, delimiter='|', lineterminator='\n')

        # load stakeholder questions
        sgs = StakeholderGroup.objects.all().order_by('code')
        for sg in sgs:
            stypes = StakeholderType.objects.filter(stakeholder_group=sg).order_by('code')
            for st in stypes:
                stakeholders = Stakeholder.objects.filter(stakeholder_type=st).order_by('code')
                for s in stakeholders:
                    a_stakeholders = AssessmentStakeholder.objects.filter(assessment_id=assessment_id, stakeholder=s)
                    for a_s in a_stakeholders:

                        if not a_s.engagement_from_local_gov:
                            a_s.engagement_from_local_gov = ""
                        else:
                            new_response = ""
                            choices_ids = get_list_of_ids(a_s.engagement_from_local_gov)
                            for id in choices_ids:
                                new_response += ChoicesStakeholders.objects.get(id=id).name + ","
                            a_s.engagement_from_local_gov = new_response
                        if not a_s.engagement_to_local_gov:
                            a_s.engagement_to_local_gov = ""
                        else:
                            new_response = ""
                            choices_ids = get_list_of_ids(a_s.engagement_to_local_gov)
                            for id in choices_ids:
                                new_response += ChoicesStakeholders.objects.get(id=id).name + ","
                            a_s.engagement_to_local_gov = new_response

                        row = [str(sg.name), str(st.name), str(s.name), str(a_s.engagement_from_local_gov),
                               str(a_s.engagement_to_local_gov)]
                        writer.writerow(row)

    # close file
    f.close()

    print("extract_stakeholders_assessment.End. assessment_id: " + str(assessment_id))



def extract_hazards_assessment(assessment_id, city_name):
    print("extract_hazards_assessment.Start. assessment_id: " + str(assessment_id))
    # open file
    file_path = settings.BASE_DIR + "/extract/" + str(city_name) + "-HazardQuestions.csv"
    with open(file_path, 'w') as f:
        writer = csv.writer(f, delimiter='|', lineterminator='\n')

        # load hazard questions
        hgs = HazardGroup.objects.all().order_by('code')
        for hg in hgs:
            htypes = HazardType.objects.filter(hazard_group=hg).order_by('code')
            for ht in htypes:
                ahts = AssessmentHazardType.objects.filter(assessment_id=assessment_id, hazard_type=ht).order_by('id')
                for aht in ahts:
                    # detail info
                    if aht.risk_assessment:
                        new_response = ""
                        choices_ids = get_list_of_ids(aht.risk_assessment)
                        for id in choices_ids:
                            new_response += ChoicesSC1.objects.get(id=id).name + ","
                        aht.risk_assessment = new_response
                    else:
                        aht.risk_assessment = ""
                    if not aht.r_a_year:
                        aht.r_a_year = ""
                    if aht.contingency_plan:
                        new_response = ""
                        choices_ids = get_list_of_ids(aht.contingency_plan)
                        for id in choices_ids:
                            new_response += ChoicesSC1.objects.get(id=id).name + ","
                        aht.contingency_plan = new_response
                    else:
                        aht.contingency_plan = ""
                    if not aht.c_p_year:
                        aht.c_p_year = ""
                    if aht.subtypes:
                        subtypes = ""
                        choices_ids = get_list_of_ids(aht.subtypes)
                        for id in choices_ids:
                            ahtst = AssessmentHazardSubtype.objects.filter(id=id)[0]
                            subtypes += str(ahtst.h_subtype.name) + ","
                    else:
                        subtypes = ""
                    # causes
                    aht_causes = AssessmentHazardCause.objects.filter(a_h_type=aht, enabled=True).order_by('id')
                    causes = ""
                    for ahtc in aht_causes:
                        causes += ahtc.a_h_type_cause.hazard_type.name + ","
                    # consequences
                    aht_consequences = AssessmentHazardConsequence.objects.filter(a_h_type=aht, enabled=True).order_by('id')
                    consequences = ""
                    for ahtc in aht_consequences:
                        consequences += ahtc.a_h_type_consequence.hazard_type.name + ","
                    # impacts
                    aht_impacts = AssessmentElementImpact.objects.filter(a_h_type=aht, enabled=True).order_by('id')
                    impacts = ""
                    for ahti in aht_impacts:
                        impacts += ahti.elem_impact.description + ","


                    row = [str(hg.name), str(ht.name), str(aht.risk_assessment), str(aht.r_a_year),
                           str(aht.contingency_plan), str(aht.c_p_year), str(subtypes), str(causes),
                           str(consequences), str(impacts)]
                    writer.writerow(row)

    # close file
    f.close()
    print("extract_hazards_assessment.End. assessment_id: " + str(assessment_id))


def extract_elements_assessment(assessment_id, city_name):
    print("extract_elements_assessment.Start. assessment_id: " + str(assessment_id))
    # open file
    file_path = settings.BASE_DIR + "/extract/" + str(city_name) + "-ElementsQuestions.csv"
    with open(file_path, 'w') as f:
        writer = csv.writer(f, delimiter='|', lineterminator='\n')

        # load component questions
        components = Component.objects.all().order_by('code')
        for component in components:
            component_questions = AssessmentComponentQuestion.objects.filter(assessment_id=assessment_id,
                                                                             component=component).\
            order_by('component_id','id')

            # write component questions
            for q in component_questions:
                parent_chain = []
                parent_names = ""
                parent = q.component.parent
                while parent:
                    parent_chain.append(parent.name)
                    parent = parent.parent
                for name in reversed(parent_chain):
                    parent_names += name + " - "

                if q.choices and str(q.choices).strip() != "" and str(q.choices) != "FF":
                    q.response = get_new_response(q.choices, q.response)
                if not q.response:
                    q.response = ""

                row = [str(parent_names),
                       str(component.name),
                       str(q.question_long),
                       str(q.response)]
                writer.writerow(row)


    # close file
    f.close()
    print("extract_elements_assessment.End. assessment_id: " + str(assessment_id))


def extract_stakeholder_comments(assessment_id, city_name):
    print("extract_stakeholder_comments.Start. assessment_id: " + str(assessment_id))
    # open file
    file_path = settings.BASE_DIR + "/extract/" + str(city_name) + "-StakeholderComments.csv"
    with open(file_path, 'w') as f:
        writer = csv.writer(f, delimiter='|', lineterminator='\n')

        # load stakeholder comments
        a_stakeholders = AssessmentStakeholder.objects.filter(assessment_id=assessment_id).order_by('id')
        comments = AssessmentStakeholderComment.objects.filter(assessment_stakeholder_id__in=a_stakeholders).\
            order_by('id')
        for c in comments:

            row = [str(c.person.name),
                   str(c.date_created),
                   str(c.assessment_stakeholder.stakeholder.name),
                   str(c.comments)]
            writer.writerow(row)

    # close file
    f.close()
    print("extract_stakeholder_comments.End. assessment_id: " + str(assessment_id))


def extract_hazards_comments(assessment_id, city_name):
    print("extract_stakeholder_comments.Start. assessment_id: " + str(assessment_id))
    # open file
    file_path = settings.BASE_DIR + "/extract/" + str(city_name) + "-HazardsComments.csv"
    with open(file_path, 'w') as f:
        writer = csv.writer(f, delimiter='|', lineterminator='\n')

        # load hazard comments
        a_hts = AssessmentHazardType.objects.filter(assessment_id=assessment_id).order_by('id')
        comments = AssessmentHazardComment.objects.filter(assessment_hazard_type__in=a_hts).\
            order_by('id')
        for c in comments:
            row = [str(c.person.name),
                   str(c.date_created),
                   str(c.assessment_hazard_type.hazard_type.name),
                   str(c.comment)]
            writer.writerow(row)

    # close file
    f.close()
    print("extract_hazards_comments.End. assessment_id: " + str(assessment_id))


def extract_elements_comments(assessment_id, city_name):
    print("extract_elements_comments.Start. assessment_id: " + str(assessment_id))
    # open file
    file_path = settings.BASE_DIR + "/extract/" + str(city_name) + "-ElementsComments.csv"
    with open(file_path, 'w') as f:
        writer = csv.writer(f, delimiter='|', lineterminator='\n')

        # load elements comments
        comments = AssessmentComponentComment.objects.filter(assessment_id=assessment_id).\
            order_by('element_id','id')
        for c in comments:
            parent_name = []
            component_element = c.element.parent
            while component_element:
                parent_name.append(component_element.name)
                component_element = component_element.parent
            for name in reversed(parent_name):
                str_parent_name = name + "-"
            str_parent_name += str(c.element.name)

            row = [str(c.person.name),
                   str(c.date_created),
                   str_parent_name,
                   str(c.comment)]
            writer.writerow(row)

    # close file
    f.close()
    print("extract_elements_comments.End. assessment_id: " + str(assessment_id))


def extract_cityid_comments(assessment_id, city_name):
    print("extract_cityid_comments.Start. assessment_id: " + str(assessment_id))
    # open file
    file_path = settings.BASE_DIR + "/extract/" + str(city_name) + "-CityIDComments.csv"
    with open(file_path, 'w') as f:
        writer = csv.writer(f, delimiter='|', lineterminator='\n')

        # load elements comments
        comments = AssessmentCityIDSectionComment.objects.filter(assessment_id=assessment_id).\
            order_by('element_id','id')
        for c in comments:
            element_name = ""
            if c.element.parent:
                element_name = str(c.element.parent.name) + "-"
            element_name += str(c.element.name)

            row = [str(c.person.name),
                   str(c.date_created),
                   element_name,
                   str(c.comment)]
            writer.writerow(row)

    # close file
    f.close()
    print("extract_cityid_comments.End. assessment_id: " + str(assessment_id))



def extract_assessment_city(assessment_id, city_name):
    extract_city_id_assessment(assessment_id, city_name)
    extract_stakeholders_assessment(assessment_id, city_name)
    extract_hazards_assessment(assessment_id, city_name)
    extract_elements_assessment(assessment_id, city_name)
    extract_stakeholder_comments(assessment_id, city_name)
    extract_cityid_comments(assessment_id, city_name)
    extract_elements_comments(assessment_id, city_name)
    extract_hazards_comments(assessment_id, city_name)



if __name__ == "__main__":
    # Barcelona: assessment_id = 2
    # Ciudad Juarez: assessment_id = 7
    ########################################

    #extract_assessment_city(7, "CiudadJuarez")
    #extract_assessment_city(2, "Barcelona")

    extract_cityid_comments(7, "CiudadJuarez")


