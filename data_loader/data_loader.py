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


def load_recursive_entity(file_name, class_name):
    print("load_recursive_entity. Start: " + file_name + " - " + str(class_name))
    file_path = settings.BASE_DIR + "/files/" + file_name
    data_reader = csv.reader(open(file_path), dialect='excel-tab')
    data_reader.next()  # to skip headers row

    for row in data_reader:
        # check for parent element
        try:
            if row[2].strip() == '':
                parent_element = None
            else:
                parent_element = class_name.objects.get(name=row[2].strip())
        except:
            parent_element = class_name()
            parent_element.name = row[0].strip()
            parent_element.long_name = row[1].strip()
            parent_element.order = row[4].strip()
            parent_element.comments = row[5].strip()
            parent_element.save()
        # load element
        try:
            element = class_name.objects.get(name=row[0].strip())
            element.parent = parent_element
            element.save()
        except:
            element = class_name()
            element.name = row[0].strip()
            element.long_name = row[1].strip()
            element.order = row[4].strip()
            element.parent = parent_element
            element.save()
    print("load_recursive_entity. End: " + file_name + " - " + str(class_name))


def set_next_element(file_name, class_name):
    print("set_next_element. Start: " + file_name + " - " + str(class_name))
    file_path = settings.BASE_DIR + "/files/" + file_name
    data_reader = csv.reader(open(file_path), dialect='excel-tab')
    data_reader.next()  # to skip headers row

    for row in data_reader:
        element_name = row[0].strip()
        next_element_name = row[3].strip()
        try:
            if next_element_name != "":
                element = class_name.objects.get(name=element_name)
                next_one = class_name.objects.get(name=next_element_name)
                element.next_one = next_one
                element.save()
        except:
            print("Error in set_next_element: " + str(sys.exc_traceback))

    print("set_next_element. End: " + file_name + " - " + str(class_name))


def load_considerations_file(file_name, class_name, class_name_comment):
    print("load_comments_file. Start: " + file_name + " - " + str(class_name))
    file_path = settings.BASE_DIR + "/files/" + file_name
    data_reader = csv.reader(open(file_path), dialect='excel-tab')
    data_reader.next()  # to skip headers row
    for row in data_reader:
        try:
            element = class_name.objects.get(name=row[0].strip())
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
                section = CityIDSection.objects.get(name=row[0].strip())
        except:
            print("ERROR: " + str(sys.exc_info()))
            print("ERROR: " + str(sys.exc_traceback))
            section = CityIDSection()
            section.name = row[0].strip()
            section.save()
        # question
        question_type = row[5].strip()
        if question_type == CHAR_FIELD:
            question = CityIDQuestionCharField()
        if question_type == TEXT_FIELD:
            question = CityIDQuestionTextField()
        if question_type == UPLOAD_FIELD:
            question = CityIDQuestionUploadField()
        if question_type == SELECT_SINGLE:
            question = CityIDQuestionSelectField()
            question.choices = row[8].strip()
            question.multi = False
        if question_type == SELECT_MULTI:
            question = CityIDQuestionSelectField()
            question.choices = row[8].strip()
            question.multi = True

        question.section = section
        question.question_short = row[1].strip()
        question.question_long = row[2].strip()
        question.help_text = row[3].strip()
        question.placeholder= row[4].strip()
        question.order = row[6].strip()
        question.not_applicable = row[7].strip().upper() == YES_STR

        # TODO: creation of new version of assessment procedure!!
        question.version = AssessmentVersion.objects.order_by('-date_released')[0]
        question.save()

    print("load_city_id_file. End: " + file_name)


if __name__ == "__main__":
    load_users_file()
    load_entity_single_field_name("cities.tsv", City)
    load_entity_single_field_name("roles.tsv", Role)
    load_entity_single_field_name("mov.tsv", MoVType)
    load_entity_single_field_name("value_type.tsv", ValueType)
    load_people()
    load_assessments()
    load_entity_single_field_name("model_dimensions.tsv", Dimension)
    load_recursive_entity("CityID-Sections.tsv", CityIDSection)
    set_next_element("CityID-Sections.tsv", CityIDSection)
    load_hazards()
    load_elements()
    load_considerations_file("CityID-SectionComments.tsv", CityIDSection, CityIDSectionConsideration)
    load_city_id_file("CityID-Location.tsv")
    load_city_id_file("CityID-Population.tsv")
    load_city_id_file("CityID-Gov&Policies.tsv")
    load_city_id_file("CityID-Economy.tsv")
    load_city_id_file("CityID-BuiltEnvironment.tsv")
    load_city_id_file("CityID-Partnerships.tsv")
    load_city_id_file("CityID-PublicRelations.tsv")
    load_city_id_file("CityID-Other.tsv")










