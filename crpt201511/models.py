import os
import django.db.models
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
    description = django.db.models.TextField(null=False, blank=False)
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
    parent = django.db.models.ForeignKey('self', null=True, blank=True)


class CityIDSection(BasicName):
    """
    Represents a section of CityID
    """


class CharFieldStatement(Common):
    """
    Represents a CharField question (not linked to anything)
    """
    question = django.db.models.CharField(max_length=250)
    help_text = django.db.models.CharField(max_length=500, null=True, blank=True)
    version = django.db.models.ForeignKey(AssessmentVersion)

    class Meta:
        abstract = True


class CityIDCharFieldStatement(CharFieldStatement):
    """
    Represents a CharField question for a section of City ID
    """
    section = django.db.models.ForeignKey(CityIDSection)


class ElementCharFieldStatement(CharFieldStatement):
    """
    Represents a CharField question for an element of the urban model
    """
    element = django.db.models.ForeignKey(Element)


class TextFieldStatement(Common):
    """
    Represents a TextField question (not linked to anything)
    """
    question = django.db.models.CharField(max_length=250)
    help_text = django.db.models.CharField(max_length=500, null=True, blank=True)
    version = django.db.models.ForeignKey(AssessmentVersion)

    class Meta:
        abstract = True


class CityIDTextFieldStatement(TextFieldStatement):
    """
    Represents a TextField question for CityID section
    """
    section = django.db.models.ForeignKey(CityIDSection)


class ElementTextFieldStatement(TextFieldStatement):
    """
    Represents a TextField question for an element of the urban model
    """
    element = django.db.models.ForeignKey(Element)


"""""""""""""""""""""""""""""""""""""""

Assessment

"""""""""""""""""""""""""""""""""""""""


class Assessment(BasicName):
    """
    Represents a City Assessment
    """
    considerations = django.db.models.TextField()
    version = django.db.models.ForeignKey(AssessmentVersion)
    city = django.db.models.ForeignKey(City)
    date_started = django.db.models.DateField(auto_now=True)
    focal_point_started = django.db.models.ForeignKey(Person)


class AssessmentCityIDCharFieldQuestion(Common):
    """
    Represents a question for CityID in an assessment
    """
    assessment = django.db.models.ForeignKey(Assessment)
    statement = django.db.models.ForeignKey(CityIDCharFieldStatement)
    value = django.db.models.CharField(max_length=500, null=True, blank=True)


class AssessmentCityIDTextFieldQuestion(Common):
    """
    Represents a question for CityID in an assessment
    """
    assessment = django.db.models.ForeignKey(Assessment)
    statement = django.db.models.ForeignKey(CityIDTextFieldStatement)
    value = django.db.models.TextField(null=True, blank=True)