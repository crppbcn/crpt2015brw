# from __future__ import unicode_literals

import csv
import sys
import os

import datetime


from django.conf import settings

project_path = "/Users/miquel/UN/0003-CRPTDEV/CRPT201511_BRW/"
sys.path.append(project_path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'crpt201511.settings'


# OBS: to initialize Django in 1.7 and run python scripts. Do not include 'setup' in installed_apps
import django
django.setup()

from django.contrib.auth.models import User, Group
from crpt201511.models import *
from crpt201511.constants import *
from crpt201511.utils.component_question_utils import *


def load_users_file():
    """
    Load into database users for cities in users.csv file
    :return:
    """
    print("load_users_file. Start..")
    file_path = settings.BASE_DIR + "/files/users.tsv"
    data_reader = csv.reader(open(file_path), dialect='excel-tab')
    data_reader.next()  # to skip headers row
    for row in data_reader:
        # read data from line
        username = row[0].strip()
        pwd = row[1].strip()
        email = row[2].strip()
        group_name = row[3].strip()
        first_name = row[4].strip()
        last_name = row[5].strip()
        # check before creation
        try:
            user = User.objects.get(username=username)
            print("User yet exists: " + row[0].strip())
        except:
            print("User does not exist: " + row[0].strip())
            user = User.objects.create_user(username, email, pwd)
        # create/update  user and eventually new group
        try:
            group = get_user_group(group_name)

            user.first_name = first_name
            user.last_name = last_name
            user.save()
            user.groups.add(group)
        except:
            print("Error creating user: " + username)
            print("Unexpected error:", sys.exc_info())
    print("load_users_file. End....")


def get_user_group(group_name):
    """
    gets or create a user group
    :param group_name:
    :return:
    """
    try:
        group = Group.objects.get(name=group_name)
        return group
    except:
        print("Group does not exist: " + group_name)
        try:
            group = Group()
            group.name = group_name
            group.save()
            print("Group created: " + group_name)
            return group
        except:
            print("Error creating group: " + group_name)


def load_entity_single_field_name(file_name, class_name):
    """
    Load file of entities with a single field name
    :param file_name:
    :param class_name:
    :return:
    """
    print("load_entity_single_field_name: " + file_name + " .Start...")
    file_path = settings.BASE_DIR + "/files/" + file_name
    data_reader = csv.reader(open(file_path), dialect='excel-tab')
    for row in data_reader:
        entity = class_name()
        entity.name = row[0].strip()
        try:
            entity.save()
        except:
            print("Unexpected error:", sys.exc_info())
    print("load_entity_single_field_name: " + file_name + " .End.")


def load_people():
    """
    Load persons file
    :return:
    """
    print("load_people. Start...")
    file_path = settings.BASE_DIR + "/files/" + "people.tsv"
    data_reader = csv.reader(open(file_path), dialect='excel-tab')
    data_reader.next()  # to skip headers row
    for row in data_reader:
        # check if user exists. if not trace and skip row
        try:
            try:
                user = User.objects.get(username=row[4].strip())
                print("username: " + row[4].strip())
            except:
                print("User does not exist: " + row[6].strip())
                print("Unexpected error:", sys.exc_info())

            # check if person exists to update it. If not, create it
            try:
                person = Person.objects.get(user=user)
                print("Person exists: " + person.name)
            except:
                print("Person does not exist: " + user.username)
                person = Person()
            person.title = row[0].strip()
            person.phone_no = row[1].strip()
            person.email = row[2].strip()
            try:
              person.city = City.objects.get(name=row[3].strip())
            except:
                print("City does not exist: " + row[3].strip())
            person.personal_title = row[5].strip()
            person.first_name = row[6].strip()
            person.last_name = row[7].strip()
            person.name = person.last_name + ", " + person.first_name
            # update user
            person.user = user
            # update role
            try:
                person.role = Role.objects.get(name=row[8].strip())
            except:
                print("Role does not exist: " + row[8].strip())
            # save person
            person.save()
        except:
            print("Unexpected error:", sys.exc_info())
    print("load_people. End.")


def load_assessments():
    """
    Load persons file
    :return:
    """
    print("load_assessments. Start.")
    file_path = settings.BASE_DIR + "/files/" + "assessments.tsv"
    data_reader = csv.reader(open(file_path), dialect='excel-tab')
    data_reader.next()  # to skip headers row
    for row in data_reader:
        assessment = AssessmentVersion()
        assessment.name = row[1].strip()
        assessment.version = row[0].strip()
        assessment.description = row[2].strip()
        assessment.date_released = datetime.datetime.strptime(row[3].strip(), "%d/%m/%Y").date()
        assessment.save()
    print("load_assessments. End.")


def load_hazards():
    """
    Load hazards file
    :return:
    """
    print("load_hazards. Start.")
    file_path = settings.BASE_DIR + "/files/" + "Hazards - Hazards.tsv"
    data_reader = csv.reader(open(file_path), dialect='excel-tab')
    data_reader.next()  # to skip headers row

    for row in data_reader:
        # check for hazard group. if not found create it
        try:
            hazard_group = HazardGroup.objects.get(code=row[0].strip())
        except:
            hazard_group = HazardGroup()
            hazard_group.code = row[0].strip()
            hazard_group.name = row[1].strip()
            hazard_group.save()
        # check for hazard type. if not found create it
        try:
            hazard_type = HazardType.objects.get(code=row[2].strip())
        except:
            hazard_type = HazardType()
            hazard_type.code = row[2].strip()
            hazard_type.name = row[3].strip()
            hazard_type.hazard_group = hazard_group
            hazard_type.save()
        # check for hazard subtype. if not found create it
        try:
            hazard_subtype = HazardSubtype.objects.get(code=row[4].strip())
        except:
            hazard_subtype = HazardSubtype()
            hazard_subtype.code = row[4].strip()
            hazard_subtype.name = row[5].strip()
            hazard_subtype.hazard_type = hazard_type
            hazard_subtype.save()
        # check for hazard subtype detail. if not found create it
        if row[6].strip() != "":
            try:
                hazard_subtype_detail = HazardSubtypeDetail.objects.get(code=row[6].strip())
            except:
                hazard_subtype_detail = HazardSubtypeDetail()
                hazard_subtype_detail.code = row[6].strip()
                hazard_subtype_detail.name = row[7].strip()
                hazard_subtype_detail.hazard_subtype = hazard_subtype
                hazard_subtype_detail.save()

    print("load_hazards. End.")


def load_hazard_type_descriptions():
    """
    Loading of hazard_type descriptions
    :return:
    """
    print("load_hazard_type_descriptions. Start.")
    file_path = settings.BASE_DIR + "/files/" + "Hazards - HazardType Descriptions.tsv"
    data_reader = csv.reader(open(file_path), dialect='excel-tab')
    data_reader.next()  # to skip headers row

    for row in data_reader:
        # check for hazard type. if not found create it
        try:
            print("looking for hazard: " + row[0].strip())
            hazard_type = HazardType.objects.get(code=row[0].strip())
            hazard_type.description = row[1].strip()
            hazard_type.save()
        except:
            print("hazard_type not found: " + row[0].strip())
            print(sys.exc_info())

    print("load_hazard_type_descriptions. End.")


def load_hazard_subtype_explanations():
    """
    Loading of hazard subtype explanations
    :return:
    """
    print("load_hazard_subtype_explanations. Start.")
    file_path = settings.BASE_DIR + "/files/" + "Hazards - HazardSubtype Examples.tsv"
    data_reader = csv.reader(open(file_path), dialect='excel-tab')
    data_reader.next()  # to skip headers row

    for row in data_reader:
        # check for hazard type. if not found create it
        try:
            hs = HazardSubtype.objects.get(code=row[0].strip())
            hs_fe = HazardSubtypeFurtherExplanation()
            hs_fe.hazard_subtype = hs
            hs_fe.description = row[1].strip()
            hs_fe.save()
        except:
            print("hazard_subtype not found: " + row[0].strip())
            print(sys.exc_info())

    print("load_hazard_subtype_explanations. End.")


def load_elements_impacted():
    """
    Loads the possible impacts on element systems
    :return:
    """
    print("load_elements_impacted. Start.")
    file_path = settings.BASE_DIR + "/files/" + "Hazards - Element Impacted.tsv"
    data_reader = csv.reader(open(file_path), dialect='excel-tab')
    data_reader.next()  # to skip headers row
    for row in data_reader:
        # check for element
        print("looking for element: " + row[0].strip())
        sys.stdout.flush()
        element = Element.objects.get(code=row[0].strip())
        # create impact
        ei = ElementImpact()
        ei.element = element
        ei.description = row[2].strip()
        ei.save()
    print("load_elements_impacted. Start.")


def load_stakeholder_groups():
    """
    Loads the stakeholder groups
    :return:
    """
    print("load_stakeholder_groups. Start.")
    file_path = settings.BASE_DIR + "/files/" + "Stakeholders - Groups.tsv"
    data_reader = csv.reader(open(file_path), dialect='excel-tab')
    data_reader.next()  # to skip headers row

    for row in data_reader:
        hg = StakeholderGroup()
        hg.code = row[0].strip()
        hg.name = row[1].strip()
        hg.description = row[2].strip()
        hg.save()
    print("load_stakeholder_groups. End.")


def set_next_stakeholder_group():
    """
    Sets next stakeholder group
    :return:
    """
    print("set_next_stakeholder_group. Start.")
    file_path = settings.BASE_DIR + "/files/" + "Stakeholders - Groups.tsv"
    data_reader = csv.reader(open(file_path), dialect='excel-tab')
    data_reader.next()  # to skip headers row

    for row in data_reader:

        if row[3].strip() != "":
            print("looking for stakeholdergroup: " + row[3].strip())
            sg = StakeholderGroup.objects.get(code=row[0].strip())
            sg.next_one = StakeholderGroup.objects.get(code=row[3].strip())
            sg.save()
    print("set_next_stakeholder_group. End.")


def load_stakeholder_considerations():
    """
    Loads stakeholder considerations
    :return:
    """
    print("load_stakeholder_considerations. Start.")
    file_path = settings.BASE_DIR + "/files/" + "Stakeholders - Considerations.tsv"
    data_reader = csv.reader(open(file_path), dialect='excel-tab')
    data_reader.next()  # to skip headers row

    for row in data_reader:
        hg = StakeholderGroup.objects.get(code=row[0].strip())

        hgc = StakeholderGroupConsideration()
        hgc.stakeholder_group = hg
        hgc.description = row[1].strip()
        hgc.save()

    print("load_stakeholder_considerations. End.")


def load_stakeholder_types():
    """
    Loads stakeholder types and subtypes
    :return:
    """
    print("load_stakeholder_types. Start.")
    file_path = settings.BASE_DIR + "/files/" + "Stakeholders - Types.tsv"
    data_reader = csv.reader(open(file_path), dialect='excel-tab')
    data_reader.next()  # to skip headers row

    for row in data_reader:
        sg = StakeholderGroup.objects.get(code=row[0].strip())
        try:
            st = StakeholderType.objects.get(code=row[1].strip())
        except:
            st = StakeholderType()
            st.stakeholder_group = sg
            st.code = row[1].strip()
            st.name = row[3].strip()
            st.help_text = row[4].strip()
            st.save()
        s = Stakeholder()
        s.stakeholder_type = st
        s.code = row[5].strip()
        s.stakeholder_type = st
        s.name = row[6].strip()
        s.help_text = row[7].strip()
        s.save()

    print("load_stakeholder_types. End.")


def set_stakeholder_next():
    """
    Sets next for stakeholders
    :return:
    """
    print("set_stakeholder_next. Start.")
    file_path = settings.BASE_DIR + "/files/" + "Stakeholders - Types.tsv"
    data_reader = csv.reader(open(file_path), dialect='excel-tab')
    data_reader.next()  # to skip headers row

    for row in data_reader:

        if row[2].strip() != "":
            st = StakeholderType.objects.get(code=row[1].strip())
            st.next_one = StakeholderType.objects.get(code=row[1].strip())
            st.save()

        if row[8].strip() != "":
            s = Stakeholder.objects.get(code=row[5].strip())
            next_one = Stakeholder.objects.get(code=row[8].strip())
            s.next_one = next_one
            s.save()

    print("set_stakeholder_next. End.")



def load_elements():
    """
    Load elements file
    :return:
    """
    print("load_elements. Start.")
    file_path = settings.BASE_DIR + "/files/" + "elements.tsv"
    data_reader = csv.reader(open(file_path), dialect='excel-tab')
    data_reader.next()  # to skip headers row

    # TODO: set version
    version = AssessmentVersion.objects.order_by('-date_released')[0]
    for row in data_reader:
        # check for parent element
        try:
            if row[1].strip() == '':
                parent_element = None
            else:
                parent_element = Element.objects.get(name=row[1].strip())
        except:
            parent_element = Element()
            parent_element.name = row[1].strip()
            parent_element.version = version
            parent_element.save()
        # load hazard
        try:
            element = Element.objects.get(name=row[0].strip())
            element.parent = parent_element
            element.version = version
            element.save()
        except:
            element = Element()
            element.name = row[0].strip()
            element.parent = parent_element
            element.version = version
            element.save()

    print("load_elements. End.")


def load_city_id_sections(file_name, class_name):
    print("load_city_id_sections. Start: " + file_name + " - " + str(class_name))
    file_path = settings.BASE_DIR + "/files/" + file_name
    data_reader = csv.reader(open(file_path), dialect='excel-tab')
    data_reader.next()  # to skip headers row

    for row in data_reader:
        # check for parent element
        try:
            if row[3].strip() == '':
                parent_element = None
            else:
                parent_element = class_name.objects.get(code=row[3].strip())
        except:
            parent_element = class_name()
            parent_element.code = row[0].strip()
            parent_element.name = row[1].strip()
            parent_element.long_name = row[2].strip()
            parent_element.order = row[5].strip()
            parent_element.save()
        # load element
        try:
            element = class_name.objects.get(code=row[0].strip())
            element.parent = parent_element
            element.save()
        except:
            element = class_name()
            element.code = row[0].strip()
            element.name = row[1].strip()
            element.long_name = row[2].strip()
            element.order = row[5].strip()
            element.parent = parent_element
            element.save()
    print("load_city_id_sections. End: " + file_name + " - " + str(class_name))


def set_next_element(file_name, class_name, next_element_field):
    print("set_next_element. Start: " + file_name + " - " + str(class_name))
    file_path = settings.BASE_DIR + "/files/" + file_name
    data_reader = csv.reader(open(file_path), dialect='excel-tab')
    data_reader.next()  # to skip headers row

    for row in data_reader:
        element_code = row[0].strip()
        next_element_code = row[next_element_field].strip()
        try:
            print("element_code: " + element_code)
            print("next_element_code: " + next_element_code)
            if next_element_code != "":
                element = class_name.objects.get(code=element_code)
                next_one = class_name.objects.get(code=next_element_code)
                element.next_one = next_one
                element.save()
        except:
            print("Error in set_next_element: " + str(sys.exc_info()))
            print("Error in set_next_element: " + str(sys.exc_traceback))

    print("set_next_element. End: " + file_name + " - " + str(class_name))


def load_considerations_file(file_name, class_name, class_name_comment):
    print("load_comments_file. Start: " + file_name + " - " + str(class_name))
    file_path = settings.BASE_DIR + "/files/" + file_name
    data_reader = csv.reader(open(file_path), dialect='excel-tab')
    data_reader.next()  # to skip headers row
    for row in data_reader:
        try:
            element = class_name.objects.get(code=row[0].strip())
            comment = class_name_comment()
            comment.comment = row[1].strip()
            comment.element = element
            comment.save()
        except:
            print("Error setting comment " + row[0].strip() + "-" + row[1].strip())

    print("load_comments_file. End: " + file_name + " - " + str(class_name))


def load_city_id_file(file_name):
    print("load_city_id_file. Start: " + file_name)
    file_path = settings.BASE_DIR + "/files/" + file_name
    data_reader = csv.reader(open(file_path), dialect='excel-tab')
    data_reader.next()  # to skip headers row
    for row in data_reader:
        # section
        try:
            if row[0].strip() == '':
                section = None
            else:
                print("Looking for section: " + row[0].strip())
                section = CityIDSection.objects.get(code=row[0].strip())
        except:
            print("ERROR: " + str(sys.exc_info()))
            print("ERROR: " + str(sys.exc_traceback))
            section = CityIDSection()
            section.code = row[0].strip()
            section.save()
        # question

        question = CityIDQuestion()
        question.question_type = row[6].strip()
        question.section = section
        question.question_short = row[2].strip()
        question.question_long = row[3].strip()
        if question.question_long.strip() == "" and question.question_short.strip() != "":
            question.question_long = question.question_short
        question.help_text = row[4].strip()
        question.placeholder= row[5].strip()
        question.order = row[7].strip()
        question.not_applicable = row[8].strip().upper() == YES_STR
        question.choices = row[9].strip().upper()
        question.multi = row[9].strip().upper() == SELECT_MULTI
        if len(row) >= 11:
            if row[10].strip() != "":
                try:
                    print("Looking for element: " + str(row[10].strip()))
                    question.element = Element.objects.get(name=row[10].strip())
                except:
                    print("Element not found: " + str(row[10].strip()))
        # TODO: creation of new version of assessment procedure!!
        question.version = AssessmentVersion.objects.order_by('-date_released')[0]
        question.save()

    print("load_city_id_file. End: " + file_name)


def load_indicator_components(file_name, class_name):
    print("load_indicator_components. End: " + file_name)
    file_path = settings.BASE_DIR + "/files/" + file_name
    data_reader = csv.reader(open(file_path), dialect='excel-tab')
    data_reader.next()  # to skip headers row

    assesment_version = AssessmentVersion.objects.order_by('-date_released')[0]

    for row in data_reader:
        # check for parent element
        if row[4].strip() == '' or row[4].strip() == "0":
            # create component for layout purposes
            print("processing parent element: " + row[0].strip())
            parent_element = class_name()
            parent_element.assessment_version = assesment_version
            parent_element.code = row[0].strip()
            if row[1].strip() != "":
                parent_element.name = row[1].strip()
            else:
                parent_element.name = row[2].strip()
            parent_element.long_name = row[2].strip()
            parent_element.description = row[3].strip()
            parent_element.order = row[6].strip()
            if row[7].strip() != "" and row[7].strip() != "0":
                parent_element.dimension = Dimension.objects.get(name=row[7].strip())
            if row[8].strip() != "#N/A":
                parent_element.data_source = row[8].strip()
            parent_element.comment = row[11].strip()
            parent_element.add_type = int(row[10].strip().upper() == YES_STR)
            parent_element.save()
            # create element for scoring purposes
            if not parent_element.dimension:
                new_element = Element()
                print("Creating parent element: " + parent_element.name)
                new_element.order = parent_element.order
                new_element.code = parent_element.code
                new_element.name = parent_element.name
                new_element.version = parent_element.assessment_version
                new_element.save()
        else:
            try:
                parent_element = class_name.objects.get(code=row[4].strip())
            except:
                print("Parent element not found: " + parent_element.name)
            # load element
            try:
                # creation of component for layout purposes
                print("processing element: " + row[0].strip())
                print("with parent element: " + parent_element.name)
                element = class_name()
                element.assessment_version = assesment_version
                element.parent = parent_element
                element.code = row[0].strip()
                if row[1].strip() != "":
                    element.name = row[1].strip()
                else:
                    element.name = row[2].strip()
                element.long_name = row[2].strip()
                element.description = row[3].strip()
                element.order = row[6].strip()
                if row[7].strip() != "" and row[7].strip() != "0":
                    element.dimension = Dimension.objects.get(name=row[7].strip())
                if row[8].strip() != "#N/A":
                    element.data_source = row[8].strip()
                element.comment = row[11].strip()
                element.add_type = int(row[10].strip().upper() == YES_STR)
                element.save()
                # creation of element for scoring purposes
                new_element = Element()
                print("Creating element: " + element.name)
                new_element.name = element.name
                new_element.order = element.order
                new_element.code = element.code
                new_element.version = element.assessment_version
                new_element.parent = Element.objects.get(code=element.parent.code)
                new_element.save()
            except:
                print("Error processing element: " + row[0].strip())
                print("With parent: " + row[4].strip())
                print(sys.exc_info())
    print("load_indicator_components. End: " + file_name)


def load_considerations_examples_file(file_name, class_name, class_name_consideration):
    print("load_considerations_examples_file. Start: " + file_name + " - " + str(class_name))
    file_path = settings.BASE_DIR + "/files/" + file_name
    data_reader = csv.reader(open(file_path), dialect='excel-tab')
    data_reader.next()  # to skip headers row
    consideration_type = None
    for row in data_reader:
        try:
            element = class_name.objects.get(code=row[0].strip())
            consideration = class_name_consideration()
            if consideration_type != row[1].strip():
                consideration_type = row[1].strip()
                consideration.show_separator = True
            consideration.type = row[1].strip()
            consideration.comment = row[3].strip()
            consideration.element = element
            consideration.save()
        except:
            print("Error setting consideration/example " + row[0].strip() + "-" + row[2].strip())
            print(sys.exc_info())

    print("load_considerations_examples_file. End: " + file_name + " - " + str(class_name))


def load_component_file(file_name):
    print("load_component_file. Start: " + file_name)
    file_path = settings.BASE_DIR + "/files/" + file_name
    data_reader = csv.reader(open(file_path), dialect='excel-tab')
    data_reader.next()  # to skip headers row
    for row in data_reader:
        # section
        try:
            if row[0].strip() == '':
                component = None
            else:
                print("Looking for component: " + row[0].strip())
                component = Component.objects.get(code=row[0].strip())
        except:
            print("ERROR: " + str(sys.exc_info()))
            print("ERROR: " + str(sys.exc_traceback))
        # question
        question_type = row[5].strip()
        question = ComponentQuestion()
        question.question_type = row[5].strip()
        question.multi = question_type == SELECT_MULTI
        question.choices = row[8].strip()
        question.component = component
        question.question_short = row[1].strip()
        question.question_long = row[2].strip()
        question.help_text = row[3].strip()
        question.placeholder= row[4].strip()
        question.order = row[6].strip()
        question.units = int(row[11].strip().upper() == YES_STR or row[11].strip().upper() == Y_STR)
        question.not_applicable = row[7].strip().upper() == YES_STR
        question.mov_position = -1 # questions that are not MoV
        # control of "add" questions
        if row[12].strip().upper() != "" and row[12].strip().upper() != NO_STR:
            question.add_type = ADD_TYPE_LGJ
        # dimension
        question.dimension = Dimension.objects.get(name=row[10].strip())
        # get element from code of component.parent, as code of questions if for layout purposes and links with
        # component that is one level under system element
        if component and component.parent:
            print("looking for component.parent with code: " + str(component.parent.code))
            element = Element.objects.get(code=component.parent.code)
            question.element = element

        # control of mov_type
        mov_txt = row[9].strip().upper()
        if mov_txt == "" or mov_txt == "0":
            mov_txt = MOV_NOT
        question.mov_type = mov_txt

        # TODO: creation of new version of assessment procedure!!
        question.version = AssessmentVersion.objects.order_by('-date_released')[0]
        question.save()

        # treatment of units - creation of additional question if needed
        units_treatment(question)

        # treatment of MoV - creation of additional questions if needed
        mov_treatment(question)

    print("load_component_file. End: " + file_name)


def load_master_data():

    load_users_file()
    load_entity_single_field_name("cities.tsv", City)
    load_entity_single_field_name("roles.tsv", Role)
    load_entity_single_field_name("dimensions.tsv", Dimension)
    load_entity_single_field_name("mov.tsv", MoVType)
    load_entity_single_field_name("value_type.tsv", ValueType)
    load_people()
    load_assessments()
    load_entity_single_field_name("CityID Options - GAS_SUPPLY.tsv", ChoicesGasSupply)
    load_entity_single_field_name("CityID Options - CITY_ROLE.tsv", ChoicesCityRole)
    load_entity_single_field_name("CityID Options - ROAD_TX.tsv", ChoicesRoadTx)
    load_entity_single_field_name("CityID Options - RAIL_TX.tsv", ChoicesRailTx)
    load_entity_single_field_name("CityID Options - WATER_TX.tsv", ChoicesWaterTx)
    load_entity_single_field_name("CityID Options - AIR_TX.tsv", ChoicesAirTx)
    load_entity_single_field_name("CityID Options - OTHER_TX.tsv", ChoicesOtherTx)
    load_entity_single_field_name("mov_scale.tsv", ChoicesMoVScale)
    load_entity_single_field_name("mov_source.tsv", ChoicesMoVSource)
    load_entity_single_field_name("MC1.tsv", ChoicesMC1)
    load_entity_single_field_name("MC2.tsv", ChoicesMC2)
    load_entity_single_field_name("MC3.tsv", ChoicesMC3)
    load_entity_single_field_name("MC4.tsv", ChoicesMC4)
    load_entity_single_field_name("SC1.tsv", ChoicesSC1)
    load_entity_single_field_name("SC2.tsv", ChoicesSC2)
    load_entity_single_field_name("SC3.tsv", ChoicesSC3)
    load_entity_single_field_name("SC4.tsv", ChoicesSC4)
    load_entity_single_field_name("SC5.tsv", ChoicesSC5)
    load_entity_single_field_name("SC6.tsv", ChoicesSC6)
    load_entity_single_field_name("SC7.tsv", ChoicesSC7)
    load_entity_single_field_name("SC8.tsv", ChoicesSC8)
    load_entity_single_field_name("SC9.tsv", ChoicesSC9)
    load_entity_single_field_name("SC11.tsv", ChoicesSC11)
    load_entity_single_field_name("SC12.tsv", ChoicesSC12)
    load_entity_single_field_name("SC13.tsv", ChoicesSC13)
    load_entity_single_field_name("SC14.tsv", ChoicesSC14)
    load_entity_single_field_name("SC15.tsv", ChoicesSC15)
    load_entity_single_field_name("SC21.tsv", ChoicesSC21)
    load_entity_single_field_name("StakeholderOptions.tsv", ChoicesStakeholders)


if __name__ == "__main__":

    # load master data
    #load_master_data()

    # Indicators
    #load_indicator_components("Indicators - Components.tsv", Component)
    #set_next_element("Indicators - Components.tsv", Component, 5)


    load_component_file("Indicators - Basic Infrastructure.tsv")
    load_component_file("Indicators - Built Environment.tsv")
    load_component_file("Indicators - Economy.tsv")
    load_component_file("Indicators - Environment.tsv")
    load_component_file("Indicators - Governance.tsv")
    load_component_file("Indicators - Public Services.tsv")
    load_component_file("Indicators - Social.tsv")
    load_component_file("Indicators - Transport.tsv")
    """
    load_considerations_examples_file("Indicators - Considerations&Examples.tsv", Component, ComponentConsideration)


    # load hazards
    load_hazards()
    load_hazard_type_descriptions()
    load_hazard_subtype_explanations()
    load_elements_impacted()

    # CityID
    load_city_id_sections("CityID - Sections.tsv", CityIDSection)
    set_next_element("CityID - Sections.tsv", CityIDSection, 4)
    load_considerations_file("CityID - SectionComments.tsv", CityIDSection, CityIDSectionConsideration)

    load_city_id_file("CityID - Location.tsv")
    load_city_id_file("CityID - Population.tsv")
    load_city_id_file("CityID - Gov. & Policies.tsv")
    load_city_id_file("CityID - Economy.tsv")
    load_city_id_file("CityID - Built Environment.tsv")
    load_city_id_file("CityID - Partnerships.tsv")
    load_city_id_file("CityID - Public Relations.tsv")
    load_city_id_file("CityID - Other.tsv")

    # load_stakeholders
    load_stakeholder_groups()
    set_next_stakeholder_group()
    load_stakeholder_considerations()
    load_stakeholder_types()
    set_stakeholder_next()

"""






