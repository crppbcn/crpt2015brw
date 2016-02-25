# from __future__ import unicode_literals

import csv
import sys
import os

import datetime


from django.conf import settings

project_path = "/Users/miquel/UN/0003-CRPTDEV/CRPT201511/"
sys.path.append(project_path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'crpt201511.settings'


# OBS: to initialize Django in 1.7 and run python scripts. Do not include 'setup' in installed_apps
import django
django.setup()

from django.contrib.auth.models import User, Group
from crpt201511.models import *
from crpt201511.constants import *


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
    file_path = settings.BASE_DIR + "/files/" + "hazards.tsv"
    data_reader = csv.reader(open(file_path), dialect='excel-tab')
    data_reader.next()  # to skip headers row

    for row in data_reader:
        # check for hazard category
        try:
            hazard_category = HazardCategory.objects.get(name=row[1].strip())
        except:
            hazard_category = HazardCategory()
            hazard_category.name = row[1].strip()
            hazard_category.save()
        # load hazard
        hazard = Hazard()
        hazard.name = row[0].strip()
        hazard.hazard_category = hazard_category
        hazard.save()

    print("load_hazards. End.")


def load_elements():
    """
    Load elements file
    :return:
    """
    print("load_elements. Start.")
    file_path = settings.BASE_DIR + "/files/" + "elements.tsv"
    data_reader = csv.reader(open(file_path), dialect='excel-tab')
    data_reader.next()  # to skip headers row

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
            parent_element.save()
        # load hazard
        try:
            element = Element.objects.get(name=row[0].strip())
            element.parent = parent_element
            element.save()
        except:
            element = Element()
            element.name = row[0].strip()
            element.parent = parent_element
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
        question_type = row[6].strip()
        if question_type == CHAR_FIELD:
            question = CityIDQuestionCharField()
        if question_type == TEXT_FIELD:
            question = CityIDQuestionTextField()
        if question_type == UPLOAD_FIELD:
            question = CityIDQuestionUploadField()
        if question_type == SELECT_SINGLE:
            question = CityIDQuestionSelectField()
            question.choices = row[9].strip()
            question.multi = False
        if question_type == SELECT_MULTI:
            question = CityIDQuestionSelectField()
            question.choices = row[9].strip()
            question.multi = True

        question.section = section
        question.question_short = row[2].strip()
        question.question_long = row[3].strip()
        if question.question_long.strip() == "" and question.question_short.strip() != "":
            question.question_long = question.question_short
        question.help_text = row[4].strip()
        question.placeholder= row[5].strip()
        question.order = row[7].strip()
        question.not_applicable = row[8].strip().upper() == YES_STR

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
            parent_element.save()
        else:
            try:
                parent_element = class_name.objects.get(code=row[4].strip())
            except:
                print("Parent element not found: " + row[4].strip())
            # load element
            try:
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
                element.save()
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
    for row in data_reader:
        try:
            element = class_name.objects.get(code=row[0].strip())
            consideration = class_name_consideration()
            consideration.type = EXAMPLE
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
        if question_type == CHAR_FIELD:
            question = ComponentQuestionCharField()
        if question_type == TEXT_FIELD:
            question = ComponentQuestionTextField()
        if question_type == SELECT_SINGLE:
            question = ComponentQuestionSelectField()
            question.choices = row[8].strip()
            question.multi = False
        if question_type == SELECT_MULTI:
            question = ComponentQuestionSelectField()
            question.choices = row[8].strip()
            question.multi = True

        question.component = component
        question.question_short = row[1].strip()
        question.question_long = row[2].strip()
        question.help_text = row[3].strip()
        question.placeholder= row[4].strip()
        question.order = row[6].strip()
        question.units = int(row[12].strip().upper() == YES_STR)
        question.not_applicable = row[7].strip().upper() == YES_STR
        question.mov_position = -1 # questions that are not MoV

        # TODO: creation of new version of assessment procedure!!
        question.version = AssessmentVersion.objects.order_by('-date_released')[0]
        question.save()

        # processing of units column
        if question.units == 1:
            new_question = ComponentQuestionCharField()
            new_question.component = question.component
            new_question.order = int(question.order) + 1
            new_question.not_applicable = False
            new_question.help_text = ""  # TODO: decide which help text to assign
            new_question.question_short = "Please specify units"
            new_question.question_long = "Please specify units"
            new_question.placeholder = "Specify units"
            new_question.multi = False
            new_question.version = question.version
            new_question.units = 2 # to indicate this is textbox for units
            new_question.has_mov = True # to add line separator
            new_question.mov_position = -1 # questions that are not MoV
            new_question.save()


        # processing of MoV
        mov_txt = row[10].strip()
        if mov_txt != MOV_NOT and mov_txt != "" and mov_txt != "0":
            question.has_mov = True
            question.save()
            # mov_position var for year (third column)
            mov_position_year = 1
            # codes
            add_year = True
            add_source = True
            add_scale = True
            if mov_txt == MOV_NS:
                add_scale = False
                mov_position_year = 4 # when No Scale, Year in third column
            if mov_txt == MOV_NY:
                add_year == False
            if mov_txt == MOV_NYS:
                add_scale = False
                add_year == False
            # add questions
            if add_source:
                new_question = ComponentQuestionSelectField()
                new_question.component = question.component
                new_question.order = int(question.order) + 1
                new_question.not_applicable = False
                new_question.help_text = ""  # TODO: decide which help text to assign
                new_question.question_short = "MoV Source"
                new_question.question_long = "MoV Source"
                new_question.multi = False
                new_question.choices = MOV_SOURCE
                new_question.version = question.version
                new_question.units = -1  # to indicate this textbox has nothing to do with MoV
                if mov_txt == MOV_NYS:
                    new_question.mov_position = MOV_LEFT_AND_LAST
                else:
                    new_question.mov_position = MOV_LEFT
                new_question.save()
            if add_scale:
                new_question = ComponentQuestionSelectField()
                new_question.component = question.component
                new_question.order = int(question.order) + 2
                new_question.not_applicable = False
                new_question.help_text = ""  # TODO: decide which help text to assign
                new_question.question_short = "MoV Scale"
                new_question.question_long = "MoV Scale"
                new_question.multi = False
                new_question.choices = MOV_SCALE
                new_question.version = question.version
                new_question.units = -1  # to indicate this textbox has nothing to do with MoV
                if mov_txt == MOV_ALL:
                    new_question.mov_position = MOV_LEFT
                if mov_txt == MOV_NY:
                    new_question.mov_position = MOV_LEFT_AND_LAST
                new_question.save()
            if add_year:
                new_question = ComponentQuestionCharField()
                new_question.component = question.component
                new_question.order = int(question.order) + 3
                new_question.not_applicable = False
                new_question.help_text = ""  # TODO: decide which help text to assign
                new_question.question_short = "MoV Year"
                new_question.question_long = "MoV Year"
                new_question.version = question.version
                new_question.units = -1  # to indicate this textbox has nothing to do with MoV
                if mov_txt == MOV_ALL:
                    new_question.mov_position = MOV_RIGHT
                if mov_txt == MOV_NS:
                    new_question.mov_position = MOV_RIGHT_NO_MID
                new_question.save()
        else:
            question.has_mov = False
            question.save()
    print("load_component_file. End: " + file_name)


if __name__ == "__main__":

    load_users_file()
    load_entity_single_field_name("cities.tsv", City)
    load_entity_single_field_name("roles.tsv", Role)
    load_entity_single_field_name("dimensions.tsv", Dimension)
    load_entity_single_field_name("mov.tsv", MoVType)
    load_entity_single_field_name("value_type.tsv", ValueType)
    load_people()
    load_assessments()
    load_entity_single_field_name("model_dimensions.tsv", Dimension)
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
    load_entity_single_field_name("SC1.tsv", ChoicesSC1)
    load_entity_single_field_name("SC2.tsv", ChoicesSC2)
    load_entity_single_field_name("SC3.tsv", ChoicesSC3)
    load_entity_single_field_name("SC4.tsv", ChoicesSC4)
    load_entity_single_field_name("SC5.tsv", ChoicesSC5)
    load_hazards()
    load_elements()

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

    # Indicators

    load_indicator_components("Indicators - Components.tsv", Component)
    set_next_element("Indicators - Components.tsv", Component, 5)
    load_considerations_examples_file("Indicators - Considerations&Examples.tsv", Component, ComponentConsideration)
    load_component_file("Indicators - Basic Infrastructure.tsv")










