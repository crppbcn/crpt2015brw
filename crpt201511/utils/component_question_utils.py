
import sys

from crpt201511.constants import *
from crpt201511.models import AssessmentComponentQuestionSelectField, AssessmentComponentQuestionCharField, \
    AssessmentComponentQuestionTextField, ComponentQuestionCharField, ComponentQuestionSelectField


def duplicate_new_question(initial_question_id, question_type):
    """
    duplication of a question
    :param initial_question_id:
    :param question_type:
    :return:
    """
    try:
        # get initial question and create the new one
        if question_type == SELECT_MULTI or SELECT_SINGLE:
            initial_question = AssessmentComponentQuestionSelectField.objects.get(id=initial_question_id)
            new_question = AssessmentComponentQuestionSelectField()
        elif question_type == CHAR_FIELD:
            initial_question = AssessmentComponentQuestionCharField.objects.get(id=initial_question_id)
            new_question = AssessmentComponentQuestionCharField()
        elif question_type == TEXT_FIELD:
            initial_question = AssessmentComponentQuestionTextField.objects.get(id=initial_question_id)
            new_question = AssessmentComponentQuestionTextField()
        else:
            raise Exception("Question type not found!!")
        # duplicate question
        new_question.assessment = initial_question.assessment
        new_question.component = initial_question.component
        new_question.question_long = "Please add new element to consider and set jurisdiction: "
        new_question.not_applicable = initial_question.not_applicable
        new_question.has_mov = initial_question.has_mov
        new_question.units = initial_question.units
        new_question.show_short_name = True  # to show text box to edit short name
        new_question.order = int(initial_question.order) + 1
        new_question.help_text = initial_question.help_text
        new_question.placeholder = initial_question.placeholder
        new_question.version = initial_question.version
        new_question.choices = initial_question.choices
        new_question.multi = initial_question.multi
        new_question.mov_position = initial_question.mov_position
        new_question.has_mov = initial_question.has_mov
        new_question.save()

        # processing of units field
        if new_question.units == 1:
            units_question = ComponentQuestionCharField()
            units_question.component = new_question.component
            units_question.order = int(new_question.order) + 1
            units_question.not_applicable = False
            units_question.help_text = ""  # TODO: decide which help text to assign
            units_question.question_short = "Please specify units"
            units_question.question_long = "Please specify units"
            units_question.placeholder = "Specify units"
            units_question.multi = False
            units_question.version = new_question.version
            units_question.units = 2 # to indicate this is textbox for units
            units_question.has_mov = True # to add line separator
            units_question.mov_position = -1 # questions that are not MoV
            units_question.save()


        # processing of MoV
        if new_question.mov_type != MOV_NOT and new_question.mov_type != "" and new_question.mov_type != "0":
            new_question.mov_type.has_mov = True
            new_question.mov_type.save()
            # mov_position var for year (third column)
            mov_position_year = 1
            # codes
            add_year = True
            add_source = True
            add_scale = True
            if new_question.mov_type == MOV_NS:
                add_scale = False
                mov_position_year = 4  # when No Scale, Year in third column
            if new_question.mov_type == MOV_NY:
                add_year == False
            if new_question.mov_type == MOV_NYS:
                add_scale = False
                add_year == False
            # add questions
            if add_source:
                new_mov_question = ComponentQuestionSelectField()
                new_mov_question.component = new_question.component
                new_mov_question.order = int(new_question.order) + 1
                new_mov_question.not_applicable = False
                new_mov_question.help_text = ""  # TODO: decide which help text to assign
                new_mov_question.question_short = "MoV Source"
                new_mov_question.question_long = "MoV Source"
                new_mov_question.multi = False
                new_mov_question.choices = MOV_SOURCE
                new_mov_question.version = new_question.version
                new_mov_question.units = -1  # to indicate this textbox has nothing to do with MoV
                if new_question.mov_type == MOV_NYS:
                    new_question.mov_position = MOV_LEFT_AND_LAST
                else:
                    new_question.mov_position = MOV_LEFT
                new_question.save()
            if add_scale:
                new_mov_question = ComponentQuestionSelectField()
                new_mov_question.component = new_question.component
                new_mov_question.order = int(new_question.order) + 2
                new_mov_question.not_applicable = False
                new_mov_question.help_text = ""  # TODO: decide which help text to assign
                new_mov_question.question_short = "MoV Scale"
                new_mov_question.question_long = "MoV Scale"
                new_mov_question.multi = False
                new_mov_question.choices = MOV_SCALE
                new_mov_question.version = new_question.version
                new_mov_question.units = -1  # to indicate this textbox has nothing to do with MoV
                if new_question.mov_type == MOV_ALL:
                    new_mov_question.mov_position = MOV_LEFT
                if new_question.mov_type == MOV_NY:
                    new_mov_question.mov_position = MOV_LEFT_AND_LAST
                new_mov_question.save()
            if add_year:
                new_mov_question = ComponentQuestionCharField()
                new_mov_question.component = new_question.component
                new_mov_question.order = int(new_question.order) + 3
                new_mov_question.not_applicable = False
                new_mov_question.help_text = ""  # TODO: decide which help text to assign
                new_mov_question.question_short = "MoV Year"
                new_mov_question.question_long = "MoV Year"
                new_mov_question.version = new_question.version
                new_mov_question.units = -1  # to indicate this textbox has nothing to do with MoV
                if new_question.mov_type == MOV_ALL:
                    new_mov_question.mov_position = MOV_RIGHT
                if new_question.mov_type == MOV_NS:
                    new_mov_question.mov_position = MOV_RIGHT_NO_MID
                new_mov_question.save()
    except:
        print("Error duplicating question: ")
        print(sys.exc_info())
        sys.stdout.flush()


