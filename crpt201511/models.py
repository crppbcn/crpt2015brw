from __future__ import division
import os, sys
import django.db.models

from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.utils import timezone

from crpt201511.utils.models_utils import *
from crpt201511.constants import *

#######################################
#
# Basic abstract classes
#
#######################################


class Common(django.db.models.Model):
    """
    Abstract base class
    """
    # ...

    class Meta:
        abstract = True


class BasicName(Common):
    """
    Abstract base class for entities with single "name" field
    """
    name = django.db.models.CharField(max_length=250, null=False, blank=False, unique=True)

    def __unicode__(self):  # Python 3: def __str__(self):
        return self.name

    class Meta:
        abstract = True

#######################################
#
# User & roles
#
#######################################


class Role(BasicName):
    """
    Represents a user role
    """


class City(BasicName):
    """
    Represents a city
    """


class Person(BasicName):
    """
    Represents UN-Habitat Staff
    """
    phone_no = django.db.models.CharField(max_length=50, null=True, blank=True)
    email = django.db.models.CharField(max_length=100, null=False, blank=False, validators=[validate_email, ])
    city = django.db.models.ForeignKey(City, null=True, blank=True)
    user = django.db.models.ForeignKey(User)
    first_name = django.db.models.CharField(max_length=100, null=False, blank=False)
    last_name = django.db.models.CharField(max_length=100, null=True, blank=True)
    personal_title = django.db.models.CharField(max_length=5, null=True, blank=True)
    role = django.db.models.ForeignKey(Role)

#######################################
#
# Utilities: tracing
#
#######################################


class TraceAction(Common):
    """
    Represents an action traced by the system
    """
    action = django.db.models.CharField(max_length=50, null=False, blank=False)
    description = django.db.models.TextField(null=True, blank=True)
    person = django.db.models.ForeignKey(Person)
    date = django.db.models.DateTimeField(default=timezone.now, null=False, blank=False)

#######################################
#
# Master Data
#
#######################################


class Dimension(BasicName):
    """
    Represents a dimension of the model
    """


class AssessmentVersion(Common):
    """
    Represents an assessment version
    """
    version = django.db.models.CharField(max_length=25)
    name = django.db.models.CharField(max_length=250, null=True, blank=True)
    description = django.db.models.TextField(null=True, blank=True)
    date_released = django.db.models.DateField(null=False, blank=False)


class Dimension(BasicName):
    """
    Represents a dimension of the urban model
    """


class Element(Common):
    """
    Represents an element of the urban model
    """
    code = django.db.models.CharField(max_length=20)
    name = django.db.models.CharField(max_length=250, null=True, blank=True)
    order = django.db.models.IntegerField(null=True, blank=True)
    parent = django.db.models.ForeignKey('self', null=True, blank=True)
    version = django.db.models.ForeignKey(AssessmentVersion)


class CityIDSection(Common):
    """
    Represents a section of CityID
    """
    code = django.db.models.CharField(max_length=20)
    name = django.db.models.CharField(max_length=50, null=True, blank=True)
    order = django.db.models.IntegerField(null=True, blank=True)
    parent = django.db.models.ForeignKey('self', null=True, blank=True, related_name="parent_section")
    next_one = django.db.models.ForeignKey('self', null=True, blank=True, related_name="next_section")
    long_name = django.db.models.CharField(max_length=250, null=True, blank=True)


class CityIDSectionConsideration(Common):
    """
    Represents comments for a CityID Section
    """
    element = django.db.models.ForeignKey(CityIDSection)
    comment = django.db.models.CharField(max_length=500)


class ValueType(BasicName):
    """
    Represents a value type for answers of the assessment
    """

class MoVType(BasicName):
    """
    Represents a type for MoV
    """


class QuestionSimple(Common):
    """
    Represents an statement (not linked to anything)
    """
    question_short = django.db.models.CharField(max_length=150)
    question_long = django.db.models.CharField(max_length=250)
    help_text = django.db.models.CharField(max_length=500, null=True, blank=True)
    placeholder = django.db.models.CharField(max_length=250, null=True, blank=True)
    version = django.db.models.ForeignKey(AssessmentVersion)
    order = django.db.models.IntegerField(null=True, blank=True)
    choices = django.db.models.CharField(max_length=50, null=True, blank=True)
    multi = django.db.models.BooleanField(default=False)
    question_type = django.db.models.CharField(max_length=25, null=True, blank=True)
    not_applicable = django.db.models.BooleanField(default=False)

    class Meta:
        abstract = True



#######################################
#
# Hazards
#
#######################################


class Hazard(Common):
    """
    Abstract class to support hazard classes
    """
    code = django.db.models.CharField(max_length=20, unique=True)
    name = django.db.models.CharField(max_length=250)

    class Meta:
        abstract = True


class HazardGroup(Hazard):
    """
    Represents a hazard group
    """


class HazardType(Hazard):
    """
    Represents a Hazard Type
    """
    hazard_group = django.db.models.ForeignKey(HazardGroup)
    description = django.db.models.CharField(max_length=500, null=True, blank=True)


class HazardSubtype(Hazard):
    """
    Represents a Hazard Subtype
    """
    hazard_type = django.db.models.ForeignKey(HazardType)


class HazardSubtypeDetail(Hazard):
    """
    Represents a Hazard Subtype Detail
    """
    hazard_subtype = django.db.models.ForeignKey(HazardSubtype)


class HazardSubtypeFurtherExplanation(Common):
    """
    Represents a further explanation for a hazard subtype
    """
    hazard_subtype = django.db.models.ForeignKey(HazardSubtype)
    description = django.db.models.CharField(max_length=500, null=True, blank=True)


class ElementImpact(Common):
    """
    Represents an impact on a system element
    """
    element = django.db.models.ForeignKey(Element)
    description = django.db.models.CharField(max_length=250, null=True, blank=True)


#######################################
#
# CityID
#
#######################################


class CityIDQuestion(QuestionSimple):
    """
    Represents a CityID Question with base parameters
    """
    section = django.db.models.ForeignKey(CityIDSection)
    element = django.db.models.ForeignKey(Element, null=True, blank=True)


#######################################
#
# Assessment
#
#######################################

class Assessment(BasicName):
    """
    Represents a City Assessment
    """
    considerations = django.db.models.TextField()
    version = django.db.models.ForeignKey(AssessmentVersion)
    city = django.db.models.ForeignKey(City)
    date_started = django.db.models.DateField(auto_now=True)
    focal_point_started = django.db.models.ForeignKey(Person)
    organizational_score = django.db.models.DecimalField(max_digits=6, decimal_places=2, default=0)
    physical_score = django.db.models.DecimalField(max_digits=6, decimal_places=2, default=0)
    functional_score = django.db.models.DecimalField(max_digits=6, decimal_places=2, default=0)
    mov_public_knowledge_noq = django.db.models.IntegerField(default=0)
    mov_media_noq = django.db.models.IntegerField(default=0)
    mov_official_document_noq = django.db.models.IntegerField(default=0)
    degree_of_completion = django.db.models.DecimalField(max_digits=6, decimal_places=2, default=0)
    city_id_completion = django.db.models.DecimalField(max_digits=6, decimal_places=2, default=0)


#######################################
#
# Assessment - Hazards
#
#######################################
class AssessmentHazardType(Common):
    """
    Represents a hazard type in an assesment
    """
    assessment = django.db.models.ForeignKey(Assessment)
    hazard_type = django.db.models.ForeignKey(HazardType)
    risk_assessment = django.db.models.CharField(max_length=50, null=True, blank=True)
    contingency_plan = django.db.models.CharField(max_length=50, null=True, blank=True)
    enabled = django.db.models.BooleanField(default=False)


class AssessmentHazardSubtype(Common):
    """
    Represents a hazard subtype in an assesment
    """
    assessment = django.db.models.ForeignKey(Assessment)
    a_h_type = django.db.models.ForeignKey(AssessmentHazardType)
    enabled = django.db.models.BooleanField(default=False)


class AssessmentHazardCause(Common):
    """
    Represents a hazard cause in an assesment
    """
    assessment = django.db.models.ForeignKey(Assessment)
    a_h_type = django.db.models.ForeignKey(AssessmentHazardType)
    enabled = django.db.models.BooleanField(default=False)


class AssessmentHazardConsequence(Common):
    """
    Represents a hazard consequence in an assesment
    """
    assessment = django.db.models.ForeignKey(Assessment)
    a_h_type = django.db.models.ForeignKey(AssessmentHazardType)
    enabled = django.db.models.BooleanField(default=False)


class AssessmentElementImpact(Common):
    """
    Represents an impact on a system element in an assessment
    """
    a_h_type = django.db.models.ForeignKey(AssessmentHazardType)
    assessment = django.db.models.ForeignKey(Assessment)
    elem_impact = django.db.models.ForeignKey(ElementImpact)
    enabled = django.db.models.BooleanField(default=False)



#######################################
#
# Assessment - Element
#
#######################################
class AssessmentElement(Common):
    """
    Represents an element of the urban system model in the assessment
    """
    assessment = django.db.models.ForeignKey(Assessment)
    parent = django.db.models.ForeignKey('self', null=True, blank=True, related_name="parent_a_element")
    element = django.db.models.ForeignKey(Element)
    enabled = django.db.models.BooleanField(default=True)
    spatial_score = django.db.models.DecimalField(max_digits=6, decimal_places=2, default=0)
    organizational_score = django.db.models.DecimalField(max_digits=6, decimal_places=2,  default=0)
    physical_score = django.db.models.DecimalField(max_digits=6, decimal_places=2, default=0)
    functional_score = django.db.models.DecimalField(max_digits=6, decimal_places=2, default=0)
    mov_public_knowledge_noq = django.db.models.IntegerField(default=0)
    mov_media_noq = django.db.models.IntegerField(default=0)
    mov_official_document_noq = django.db.models.IntegerField(default=0)
    degree_of_completion = django.db.models.DecimalField(max_digits=6, decimal_places=2, default=0)


#######################################
#
# Assessment - City ID
#
#######################################
class AssessmentCityIDQuestion(CityIDQuestion):

    assessment = django.db.models.ForeignKey(Assessment)
    response = django.db.models.CharField(max_length=250, null=True, blank=True)
    assessment_element = django.db.models.ForeignKey(AssessmentElement, null=True, blank=True)


class AssessmentCityIDQuestionFile(Common):
    """
    Represents a single file uploaded in a question of type file upload
    """
    name = django.db.models.CharField(max_length=250, null=False, blank=False, unique=False)
    remote_folder = django.db.models.CharField(max_length=250)
    question = django.db.models.ForeignKey(AssessmentCityIDQuestion)


class AssessmentCityIDSectionComment(Common):
    """
    Represents comments for a CityID Section
    """
    assessment = django.db.models.ForeignKey(Assessment)
    element = django.db.models.ForeignKey(CityIDSection)
    comment = django.db.models.CharField(max_length=500)
    person = django.db.models.ForeignKey(Person)
    date_created = django.db.models.DateTimeField(auto_now=True)


#######################################
#
# Indicators
#
#######################################
class Component(Common):
    """
    Represents an indicator
    """
    assessment_version = django.db.models.ForeignKey(AssessmentVersion)
    code = django.db.models.CharField(max_length=20)
    name = django.db.models.CharField(max_length=50, null=True, blank=True)
    order = django.db.models.IntegerField(null=True, blank=True)
    parent = django.db.models.ForeignKey('self', null=True, blank=True, related_name="parent_element")
    next_one = django.db.models.ForeignKey('self', null=True, blank=True, related_name="next_element")
    long_name = django.db.models.CharField(max_length=250, null=True, blank=True)
    description = django.db.models.TextField(null=True, blank=True)
    dimension = django.db.models.ForeignKey(Dimension, null=True, blank=True)
    data_source = django.db.models.CharField(max_length=250, null=True, blank=True)
    comment = django.db.models.CharField(max_length=500, null=True, blank=True)
    add_type = django.db.models.IntegerField(default=0)


class ComponentConsideration(Common):
    """
    Represents comments for a CityID Section
    """
    element = django.db.models.ForeignKey(Component)
    comment = django.db.models.CharField(max_length=800)
    type = django.db.models.CharField(max_length=25)
    show_separator = django.db.models.BooleanField(default=False)


class ComponentQuestion(QuestionSimple):
    """
    Represents a Component Question with base parameters
    """

    component = django.db.models.ForeignKey(Component)
    has_mov = django.db.models.BooleanField(default=False)
    units = django.db.models.IntegerField(null=True, blank=True)
    mov_type = django.db.models.CharField(max_length=10, null=True, blank=True)
    mov_position = django.db.models.IntegerField(default=0)
    add_type = django.db.models.IntegerField(default=0)
    show_short_name = django.db.models.BooleanField(default=False)
    element = django.db.models.ForeignKey(Element)
    dimension = django.db.models.ForeignKey(Dimension)


#######################################
#
# Assessment - Component
#
#######################################


class AssessmentComponentComment(Common):
    """
    Represents comments for a component
    """
    assessment = django.db.models.ForeignKey(Assessment)
    element = django.db.models.ForeignKey(Component)
    comment = django.db.models.CharField(max_length=500)
    person = django.db.models.ForeignKey(Person)
    date_created = django.db.models.DateTimeField(auto_now=True)


class AssessmentComponentQuestion(ComponentQuestion):

    assessment = django.db.models.ForeignKey(Assessment)
    score = django.db.models.DecimalField(max_digits=6, decimal_places=2, default=0)
    weight = django.db.models.DecimalField(max_digits=6, decimal_places=2, default=0)
    response = django.db.models.CharField(max_length=250, null=True, blank=True)
    choices_length = django.db.models.IntegerField(default=0)
    assessment_element = django.db.models.ForeignKey(AssessmentElement, null=True, blank=True)
    scorable = django.db.models.BooleanField(default=False)

    # Overriding save method to calculate score. TODO: use signals to recalculate overall score?
    def save(self, *args, **kwargs):
        if str(self.response).strip() != "" and str(self.response).strip() != "''":
            # Scoring for questions with percentage. TODO: for now we assume all them will be with %
            if self.units == 1:
                try:
                    try:
                        int_response = int(self.response)
                    except:
                        int_response = 0
                    self.score = float(int_response / 10)
                except:
                    print("Error calculating score for % question")
                    print("Error: " + str(sys.exc_info()))
                    sys.stdout.flush()
            # Scoring for Select Single questions
            if self.question_type == SELECT_SINGLE and self.choices_length > 0:
                try:
                    int_response = int(self.response)
                except:
                    print("Error calculating score for SELECT_SINGLE question")
                    print("Error: " + str(sys.exc_info()))
                    sys.stdout.flush()

                    int_response = 1
                # if MoV Source only counting source types
                if self.choices == MOV_SOURCE:
                    self.score = (int_response - 1)
                else:
                    # response -1 to range from 0 to 10 as options selected begin in 1
                    self.score = (10 / self.choices_length) * (int_response - 1)
            # Scoring for Select Multiple choices questions
            if self.choices_length > 0 and self.question_type == SELECT_MULTI:
                try:
                    # obtain max selected value
                    resp_length = len(str(self.response))
                    max_selected_value = get_max_selected_value(self.response)
                except:
                    max_selected_value = 0
                    print("Error calculating score for SELECT_MULTI question")
                    print("Error: " + str(sys.exc_info()))
                    sys.stdout.flush()
                # calculate the score
                self.score = (10 / self.choices_length) * max_selected_value
        else:
            self.score = 0

        # Always call parent save method
        super(AssessmentComponentQuestion, self).save(*args, **kwargs)


#######################################
#
# Assessment choices
#
#######################################


class AssessmentCityIDChoicesOtherTx(BasicName):
    """
    Represents Other Means of Tx added by city in an assessment
    """
    assessment = django.db.models.ForeignKey(Assessment)


class AssessmentChoicesMC1(BasicName):
    """
    Represents Other Means of Tx added by city in an assessment
    """
    assessment = django.db.models.ForeignKey(Assessment)


#######################################
#
# CityID Options for select questions
#
#######################################


class ChoicesCityRole(BasicName):
    """
    Represents City Roles
    """


class ChoicesGasSupply(BasicName):
    """
    Represents Gas Supply destinations
    """


class ChoicesRoadTx(BasicName):
    """
    Represents Road Transport types
    """


class ChoicesRailTx(BasicName):
    """
    Represents Rail Transport types
    """


class ChoicesAirTx(BasicName):
    """
    Represents Rail Transport types
    """


class ChoicesWaterTx(BasicName):
    """
    Represents Water Transport types
    """


class ChoicesOtherTx(BasicName):
    """
    Represents Other Transport types
    """

#######################################
#
# Components Options for select questions
#
#######################################


class ChoicesMoVScale(BasicName):
    """
    Represents MoV Scale options
    """


class ChoicesMoVSource(BasicName):
    """
    Represents MoV Source options
    """


class ChoicesMC1(BasicName):
    """
    Represents MoV Source options
    """


class ChoicesMC2(BasicName):
    """
    Represents MoV Source options
    """


class ChoicesSC1(BasicName):
    """
    Represents MoV Source options
    """


class ChoicesSC1(BasicName):
    """
    Represents MoV Source options
    """


class ChoicesSC2(BasicName):
    """
    Represents MoV Source options
    """


class ChoicesSC3(BasicName):
    """
    Represents MoV Source options
    """


class ChoicesSC4(BasicName):
    """
    Represents MoV Source options
    """


class ChoicesSC5(BasicName):
    """
    Represents MoV Source options
    """


class ChoicesSC6(BasicName):
    """
    Represents MoV Source options
    """


class ChoicesSC7(BasicName):
    """
    Represents MoV Source options
    """


class ChoicesSC8(BasicName):
    """
    Represents MoV Source options
    """


class ChoicesSC9(BasicName):
    """
    Represents MoV Source options

    """

class ChoicesSC11(BasicName):
    """
    Represents MoV Source options
    """


class ChoicesSC12(BasicName):
    """
    Represents MoV Source options
    """


class ChoicesSC13(BasicName):
    """
    Represents MoV Source options
    """


class ChoicesSC14(BasicName):
    """
    Represents MoV Source options
    """


class ChoicesSC15(BasicName):
    """
    Represents MoV Source options
    """


class ChoicesSC21(BasicName):
    """
    Represents MoV Source options
    """

#######################################
#
# TEST
#
#######################################
class QuestionType1(Common):
    assessment = django.db.models.ForeignKey(Assessment)
    field1 = django.db.models.TextField()


class QuestionType2(Common):
    assessment = django.db.models.ForeignKey(Assessment)
    field2 = django.db.models.CharField(max_length=500, null=True, blank=True)


class QuestionType3(Common):
    assessment = django.db.models.ForeignKey(Assessment)
    field3 = django.db.models.ForeignKey(MoVType, null=True, blank=True)