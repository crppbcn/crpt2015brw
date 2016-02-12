from django.forms import HiddenInput


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
            question = form.save(commit=False)
            question.response = "Not applicable"
        except KeyError:
            # n_a field not found
            pass
