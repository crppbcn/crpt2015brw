
import sys

from crpt201511.constants import *
from crpt201511.models import *


def duplicate_question_function(initial_question_id):
    """
    duplication of a component question
    :param initial_question_id:
    :return:
    """
    try:
        # get initial question and create the new one
        initial_question = AssessmentComponentQuestion.objects.get(id=initial_question_id)
        new_question = AssessmentComponentQuestion()

        # duplicate question
        new_question.assessment = initial_question.assessment
        new_question.component = initial_question.component
        new_question.assessment_element = initial_question.assessment_element
        new_question.question_long = "Please add new element to consider: "
        new_question.not_applicable = initial_question.not_applicable
        new_question.has_mov = initial_question.has_mov
        new_question.units = initial_question.units
        new_question.show_short_name = True  # to show text box to edit short name
        new_question.order = int(initial_question.order) + 10  # to avoid problems with mov if any
        new_question.help_text = initial_question.help_text
        new_question.placeholder = initial_question.placeholder
        new_question.version = initial_question.version
        new_question.choices = initial_question.choices
        new_question.multi = initial_question.multi
        new_question.mov_position = initial_question.mov_position
        new_question.has_mov = initial_question.has_mov
        new_question.save()

        # units treatment
        units_treatment(new_question)

        # mov treatment
        mov_treatment(new_question)

    except:
        print("Error duplicating question: ")
        print(sys.exc_info())
        sys.stdout.flush()


def units_treatment(question):
    """
    Creation of new units question if needed
    :param question:
    :return:
    """
    if question.units == 1:
        new_question = ComponentQuestion()
        new_question.question_type = CHAR_FIELD
        new_question.component = question.component
        new_question.element = question.element
        new_question.dimension = question.dimension
        new_question.order = int(question.order) + 1
        new_question.not_applicable = False
        new_question.help_text = ""  # TODO: decide which help text to assign
        new_question.question_short = "Please specify units"
        new_question.question_long = "Please specify units"
        new_question.placeholder = "%"
        new_question.multi = False
        new_question.version = question.version
        new_question.units =  2 # to indicate this is textbox for units
        new_question.has_mov = True  # to add line separator
        new_question.mov_position = -1  # questions that are not MoV
        new_question.mov_type = ""
        new_question.save()


def mov_treatment(question):
    """
    Creation of new mov questions if needed
    :param question:
    :return:
    """
    if question.mov_type != MOV_NOT:
        question.has_mov = True
        question.save()
        # mov_position var for year (third column)
        mov_position_year = 1
        # codes
        add_year = True
        add_source = True
        add_scale = True
        if question.mov_type == MOV_NS:
            add_scale = False
            mov_position_year = 4  # when No Scale, Year in third column
        if question.mov_type == MOV_NY:
            add_year == False
        if question.mov_type == MOV_NYS:
            add_scale = False
            add_year == False
        # add questions - always add Source Name
        new_question = ComponentQuestion()
        new_question.question_type = CHAR_FIELD
        new_question.component = question.component
        new_question.order = int(question.order) + 2  # to avoid conflict with units questions if exists
        new_question.not_applicable = False
        new_question.help_text = ""  # TODO: decide which help text to assign
        new_question.question_short = "MoV Source"
        new_question.question_long = "MoV Source"
        new_question.multi = False
        new_question.choices = ""
        new_question.version = question.version
        new_question.units = 0  # to indicate this textbox will have col-md-12 and will be aligned left
        new_question.mov_position = -1  # to not generate more MoV in case of duplication
        new_question.mov_type = ""
        new_question.element = question.element
        new_question.dimension = question.dimension
        new_question.save()

        if add_source:
            new_question = ComponentQuestion()
            new_question.question_type = SELECT_SINGLE
            new_question.component = question.component
            new_question.order = int(question.order) + 3
            new_question.not_applicable = False
            new_question.help_text = ""  # TODO: decide which help text to assign
            new_question.question_short = "MoV Source Type"
            new_question.question_long = "MoV Source Type"
            new_question.multi = False
            new_question.choices = MOV_SOURCE
            new_question.version = question.version
            new_question.units = -1  # to indicate this textbox has nothing to do with units
            new_question.dimension = question.dimension
            if question.mov_type == MOV_NYS:
                new_question.mov_position = MOV_LEFT_AND_LAST
            else:
                new_question.mov_position = MOV_LEFT
            new_question.mov_type = ""
            new_question.element = question.element
            new_question.dimension = question.dimension
            new_question.save()
        if add_scale:
            new_question = ComponentQuestion()
            new_question.question_type = SELECT_SINGLE
            new_question.component = question.component
            new_question.order = int(question.order) + 4
            new_question.not_applicable = False
            new_question.help_text = ""  # TODO: decide which help text to assign
            new_question.question_short = "MoV Scale"
            new_question.question_long = "MoV Scale"
            new_question.multi = False
            new_question.choices = MOV_SCALE
            new_question.version = question.version
            new_question.units = -1  # to indicate this textbox has nothing to do with MoV
            if question.mov_type == MOV_ALL:
                new_question.mov_position = MOV_LEFT
            if question.mov_type == MOV_NY:
                new_question.mov_position = MOV_LEFT_AND_LAST
            new_question.mov_type = ""
            new_question.element = question.element
            new_question.dimension = question.dimension
            new_question.save()
        if add_year:
            new_question = ComponentQuestion()
            new_question.question_type = CHAR_FIELD
            new_question.component = question.component
            new_question.order = int(question.order) + 5
            new_question.not_applicable = False
            new_question.help_text = ""  # TODO: decide which help text to assign
            new_question.question_short = "MoV Year"
            new_question.question_long = "MoV Year"
            new_question.version = question.version
            new_question.units = -1  # to indicate this textbox has nothing to do with MoV
            if question.mov_type == MOV_ALL:
                new_question.mov_position = MOV_RIGHT
            if question.mov_type == MOV_NS:
                new_question.mov_position = MOV_RIGHT_NO_MID
            new_question.mov_type = ""
            new_question.element = question.element
            new_question.dimension = question.dimension
            new_question.save()
    else:
        question.has_mov = False
        question.save()


def set_max_num_of_choices(question):
    """
    Sets the max num of choices of a question
    :param question:
    :return:
    """
    # -1 to rate from 0 to 10
    if question.choices == SC1:
        question.choices_length = len(ChoicesSC1.objects.all())-1
    if question.choices == SC2:
        question.choices_length = len(ChoicesSC2.objects.all())-1
    if question.choices == SC3:
        question.choices_length = len(ChoicesSC3.objects.all())-1
    if question.choices == SC4:
        question.choices_length = len(ChoicesSC4.objects.all())-1
    if question.choices == SC5:
        question.choices_length = len(ChoicesSC5.objects.all())-1
    if question.choices == SC6:
        question.choices_length = len(ChoicesSC6.objects.all())-1
    if question.choices == SC7:
        question.choices_length = len(ChoicesSC7.objects.all())-1
    if question.choices == SC8:
        question.choices_length = len(ChoicesSC8.objects.all())-1
    if question.choices == SC9:
        question.choices_length = len(ChoicesSC9.objects.all())-1
    if question.choices == SC11:
        question.choices_length = len(ChoicesSC11.objects.all())-1
    if question.choices == SC12:
        question.choices_length = len(ChoicesSC12.objects.all())-1
    if question.choices == SC13:
        question.choices_length = len(ChoicesSC13.objects.all())-1
    if question.choices == SC14:
        question.choices_length = len(ChoicesSC14.objects.all())-1
    if question.choices == SC15:
        question.choices_length = len(ChoicesSC15.objects.all())-1
    if question.choices == SC21:
        question.choices_length = len(ChoicesSC21.objects.all())-1
    if question.choices == MOV_SOURCE:
        question.choices_length = len(ChoicesMoVSource.objects.all())-1
