import os
import django.db.models

from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.utils import timezone

"""""""""""""""""""""""""""""""""""""""

Basic abstract classes

"""""""""""""""""""""""""""""""""""""""

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

"""""""""""""""""""""""""""""""""""""""

Users & roles

"""""""""""""""""""""""""""""""""""""""


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

"""""""""""""""""""""""""""""""""""""""

Utilities: tracing

"""""""""""""""""""""""""""""""""""""""


class TraceAction(Common):
    """
    Represents an action traced by the system
    """
    action = django.db.models.CharField(max_length=50, null=False, blank=False)
    description = django.db.models.TextField(null=True, blank=True)
    person = django.db.models.ForeignKey(Person)
    date = django.db.models.DateTimeField(default=timezone.now, null=False, blank=False)

"""""""""""""""""""""""""""""""""""""""

Master Data

"""""""""""""""""""""""""""""""""""""""

class AssessmentVersion(Common):
    """
    Represents an assessment version
    """
    version = django.db.models.CharField(max_length=25)
    name = django.db.models.CharField(max_length=250, null=True, blank=True)
    description = django.db.models.TextField(null=True, blank=True)
    date_released = django.db.models.DateField(null=False, blank=False)


class HazardCategory(BasicName):
    """
    Represents a Hazard Category
    """


class Hazard(BasicName):
    """
    Represents a Hazard Category
    """
    hazard_category = django.db.models.ForeignKey(HazardCategory)


class Dimension(BasicName):
    """
    Represents a dimension of the urban model
    """


class Element(BasicName):
    """
    Represents an element of the urban model
    """
    order = django.db.models.IntegerField(null=True, blank=True)
    parent = django.db.models.ForeignKey('self', null=True, blank=True)


class CityIDSection(BasicName):
    """
    Represents a section of CityID
    """
    order = django.db.models.IntegerField(null=True, blank=True)
    parent = django.db.models.ForeignKey('self', null=True, blank=True)
    long_name = django.db.models.CharField(max_length=250, null=True, blank=True)


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

    class Meta:
        abstract = True


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

    class Meta:
        abstract = True


class CityIDQuestionCharField(CityIDQuestion):
    """
    Represents a CityID question with CharField answer
    """


class CityIDQuestionTextField(CityIDQuestion):
    """
    Represents a CityID question with CharField answer
    """


class CityIDQuestionUploadField(CityIDQuestion):
    """
    Represents a question with UploadField value
    """



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
    #TODO: status (%) of fulfillment


#######################################
#
# Assessment - City ID
#
#######################################
class AssessmentCityIDQuestion(CityIDQuestion):

    assessment = django.db.models.ForeignKey(Assessment)

    class Meta:
        abstract = True

class AssessmentCityIDQuestionCharField(AssessmentCityIDQuestion):
    """
    Links a CityIDStatement with an Assessment
    """
    response = django.db.models.CharField(max_length=250, null=True, blank=True)


class AssessmentCityIDQuestionTextField(AssessmentCityIDQuestion):
    """
    Represents a question for CityID in an assessment with value CharField
    """
    response = django.db.models.TextField(null=True, blank=True)



class AssessmentCityIDQuestionUploadField(AssessmentCityIDQuestion):
    """
    Represents a question for CityID in an assessment with value TextField
    """
    response = django.db.models.TextField(null=True, blank=True)


class AssessmentCityIDQuestionFile(BasicName):
    """
    Represents a single file uploaded in a question of type file upload
    """
    remote_folder = django.db.models.CharField(max_length=250)
    question = django.db.models.ForeignKey(AssessmentCityIDQuestionUploadField)


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