import sys
from django.forms import HiddenInput
from threading import Thread

from crpt201511.trace import *
from crpt201511.constants import TRACE_UPDATED_FIELDS


def set_form_hidden_fields(formset, fields_to_hide):
    """
    Function to set hidden fields and show fields of each form in formset
    :param formset:
    :param fields_to_hide:
    :return:
    """
    for form in formset:
        for field in form.fields:
            if field in fields_to_hide:
                form.fields[field].widget = HiddenInput()


def not_applicable_responses_treatment(formset):
    """
    processing of not applicable responses
    :param formset:
    :return:
    """
    # processing of not applicable values
    for form in formset:
        data = form.cleaned_data
        try:
            n_a = data['n_a']
            if n_a:
                question = form.save(commit=False)
                question.response = "Not applicable"
        except KeyError:
            # n_a field not found
            pass


def trace_updated_fields(formset, person, assessment):
    """
    Trace updated fields
    :param formset:
    :param person:
    :param assessment:
    :return:
    """
    updated_fields = dict()
    for form in formset:
        for field_name in form.changed_data:
            question = form.save(commit=False)
            updated_fields[question.question_short] = form.cleaned_data[field_name]

    if len(updated_fields) > 0:
        t = Thread(target=trace_action, args=(TRACE_UPDATED_FIELDS, person,
                                              "Assessment: " + assessment.name + ". Fields: " + str(updated_fields)))
        t.start()