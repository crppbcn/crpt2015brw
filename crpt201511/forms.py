from django.forms import ModelForm

import sys

from ast import literal_eval
from fields import *
from django import forms
from django.utils.encoding import *

from crpt201511.models import *

from crpt201511.constants import *


class MultiFileInput(forms.FileInput):

    def render(self, name, value, attrs={}):
        attrs['multiple'] = 'multiple'
        return super(MultiFileInput, self).render(name, None, attrs=attrs)

    def value_from_datadict(self, data, files, name):
        if hasattr(files, 'getlist'):
            return files.getlist(name)
        else:
            return [files.get(name)]


class MultiFileField(forms.FileField):

    widget = MultiFileInput
    default_error_messages = {
        'min_num': u"Ensure at least %(min_num)s files are uploaded (received %(num_files)s).",
        'max_num': u"Ensure at most %(max_num)s files are uploaded (received %(num_files)s).",
        'file_size' : u"File: %(uploaded_file_name)s, exceeded maximum upload size.",
        'file_extension': u"File: %(uploaded_file_name)s, wrong file format."
    }

    def __init__(self, *args, **kwargs):
        self.min_num = kwargs.pop('min_num', 0)
        self.max_num = kwargs.pop('max_num', None)
        self.maximum_file_size = kwargs.pop('maximum_file_size', None)
        super(MultiFileField, self).__init__(*args, **kwargs)

    def to_python(self, data):
        ret = []
        for item in data:
            ret.append(super(MultiFileField, self).to_python(item))
        return ret

    def validate(self, data):
        super(MultiFileField, self).validate(data)
        num_files = len(data)
        if len(data) and not data[0]:
            num_files = 0
        if num_files < self.min_num:
            raise ValidationError(self.error_messages['min_num'] % {'min_num': self.min_num, 'num_files': num_files})
            return data
        elif self.max_num and num_files > self.max_num:
            raise ValidationError(self.error_messages['max_num'] % {'max_num': self.max_num, 'num_files': num_files})
            return data
        for uploaded_file in data:
            if uploaded_file:
                if uploaded_file.name[len(uploaded_file.name)-3:] not in FILE_EXTENSIONS:
                    raise ValidationError(self.error_messages['file_extension'] % {'uploaded_file_name': uploaded_file.name})
                    return data
                if uploaded_file.size > self.maximum_file_size:
                    raise ValidationError(self.error_messages['file_size'] % {'uploaded_file_name': uploaded_file.name})
                    return data

"""
class AssessmentCityIDQuestionUploadFieldForm(forms.ModelForm):

    files = MultiFileField(required=False, max_num=MAX_FILES, min_num=0, maximum_file_size=MAX_FILE_MEGABYTES)

    def __init__(self, *args, **kwargs):
        super(AssessmentCityIDQuestionUploadFieldForm, self).__init__(*args, **kwargs)

        file_list = AssessmentCityIDQuestionFile.objects.filter(question_id=self.instance.id)
        i = 0
        for item in file_list:
            self.fields['file_' + str(i)] = forms.CharField(initial=item.name)
            i += 1

        # add checkbox field for not applicable option
        if self.instance:
            if self.instance.not_applicable:
                self.fields['n_a'] = forms.BooleanField(required=False, initial=False,
                                                        widget=forms.CheckboxInput(attrs={}))

    class Meta:
        model = AssessmentCityIDQuestionUploadField
        fields = '__all__'
"""


class AssessmentCityIDQuestionForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(AssessmentCityIDQuestionForm, self).__init__(*args, **kwargs)

        # set multi and choices
        if self.instance and \
                (self.instance.question_type == SELECT_SINGLE or self.instance.question_type == SELECT_MULTI):

            if self.instance.choices and self.instance.choices.strip() != "":
                if self.instance.choices == GAS_SUPPLY:
                    if self.instance.multi:
                        self.fields['response'].widget = \
                            forms.widgets.CheckboxSelectMultiple (
                                choices=tuple([a.id, a.name] for a in ChoicesGasSupply.objects.all().order_by('id')))
                    else:
                        self.fields['response'].widget = \
                            forms.widgets.Select(
                                choices=tuple([a.id, a.name] for a in ChoicesGasSupply.objects.all().order_by('id')))

                if self.instance.choices == CITY_ROLE:
                    if self.instance.multi:
                        self.fields['response'].widget = \
                            forms.widgets.CheckboxSelectMultiple(
                                choices=tuple([a.id, a.name] for a in ChoicesCityRole.objects.all().order_by('id')))
                    else:
                        self.fields['response'].widget = \
                            forms.widgets.Select(
                                choices=tuple([a.id, a.name] for a in ChoicesCityRole.objects.all().order_by('id')))

                if self.instance.choices == ROAD_TX:
                    if self.instance.multi:
                        self.fields['response'].widget = \
                            forms.widgets.CheckboxSelectMultiple(
                                choices=tuple([a.id, a.name] for a in ChoicesRoadTx.objects.all().order_by('id')))
                    else:
                        self.fields['response'].widget = \
                            forms.widgets.Select(
                                choices=tuple([a.id, a.name] for a in ChoicesRoadTx.objects.all().order_by('id')))

                if self.instance.choices == RAIL_TX:
                    if self.instance.multi:
                        self.fields['response'].widget = \
                            forms.widgets.CheckboxSelectMultiple(
                                choices=tuple([a.id, a.name] for a in ChoicesRailTx.objects.all().order_by('id')))
                    else:
                        self.fields['response'].widget = \
                            forms.widgets.Select(
                                choices=tuple([a.id, a.name] for a in ChoicesRailTx.objects.all().order_by('id')))

                if self.instance.choices == WATER_TX:
                    if self.instance.multi:
                        self.fields['response'].widget = \
                            forms.widgets.CheckboxSelectMultiple(
                                choices=tuple([a.id, a.name] for a in ChoicesWaterTx.objects.all().order_by('id')))
                    else:
                        self.fields['response'].widget = \
                            forms.widgets.Select(
                                choices=tuple([a.id, a.name] for a in ChoicesWaterTx.objects.all().order_by('id')))

                if self.instance.choices == AIR_TX:
                    if self.instance.multi:
                        self.fields['response'].widget = \
                            forms.widgets.CheckboxSelectMultiple(
                                choices=tuple([a.id, a.name] for a in ChoicesAirTx.objects.all().order_by('id')))
                    else:
                        self.fields['response'].widget = \
                            forms.widgets.Select(
                                choices=tuple([a.id, a.name] for a in ChoicesAirTx.objects.all().order_by('id')))

                if self.instance.choices == OTHER_TX:
                    if self.instance.multi:
                        self.fields['response'].widget = \
                            forms.widgets.CheckboxSelectMultiple(choices=tuple([str(a.id), a.name]for a in
                            AssessmentCityIDChoicesOtherTx.objects.filter(assessment=self.instance.assessment).order_by('id')))
                    else:
                        self.fields['response'].widget = \
                            forms.widgets.Select(choices=tuple([str(a.id), a.name] for a in
                            AssessmentCityIDChoicesOtherTx.objects.filter(assessment=self.instance.assessment).order_by('id')))
                    # setting initial value with some processing of stored string of selected values
                    if self.instance.response:
                        selected = literal_eval(self.instance.response)
                        self.initial['response'] = selected

                if self.instance.choices == SC1:
                    if self.instance.multi:
                        self.fields['response'].widget = \
                            forms.widgets.CheckboxSelectMultiple(
                                choices=tuple([a.id, a.name] for a in ChoicesSC1.objects.all().order_by('id')))
                    else:
                        self.fields['response'].widget = \
                            forms.widgets.Select(
                                choices=tuple([a.id, a.name] for a in ChoicesSC1.objects.all().order_by('id')))


                    # add field to input new option
                    self.fields['other'] = forms.CharField(label=LABEL_TAG_ANY_OTHER, max_length=250, required=False)

        # set multi and choices
        if self.instance and \
                (self.instance.question_type == UPLOAD_FIELD):

            self.fields['files'] = MultiFileField(required=False, max_num=MAX_FILES, min_num=0,
                                                  maximum_file_size=MAX_FILE_MEGABYTES)

            file_list = AssessmentCityIDQuestionFile.objects.filter(question_id=self.instance.id)
            i = 0
            if len(file_list) > 0:
                for item in file_list:
                    print("Adding file_" + str(i) + " field. form instance.id: " + str(self.instance.id))
                    self.fields['file_' + str(i)] = forms.CharField(initial=item.name, required=False)
                    i += 1

            # add checkbox field for not applicable option
            if self.instance:
                if self.instance.not_applicable:
                    self.fields['n_a'] = forms.BooleanField(required=False, initial=False,
                                                            widget=forms.CheckboxInput(attrs={}))

    class Meta:
        model = AssessmentCityIDQuestion
        fields = '__all__'


class AssessmentComponentQuestionForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(AssessmentComponentQuestionForm, self).__init__(*args, **kwargs)

        # set multi and choices
        if self.instance:

            if self.instance.choices and self.instance.choices.strip() != "":
                if self.instance.choices == MOV_SCALE:
                    if self.instance.multi:
                        self.fields['response'].widget = \
                            forms.widgets.CheckboxSelectMultiple (
                                choices=tuple([a.id, a.name] for a in ChoicesMoVScale.objects.all().order_by('id')))
                    else:
                        self.fields['response'].widget = \
                            forms.widgets.Select(
                                choices=tuple([a.id, a.name] for a in ChoicesMoVScale.objects.all().order_by('id')))

                if self.instance.choices == MOV_SOURCE:
                    if self.instance.multi:
                        self.fields['response'].widget = \
                            forms.widgets.CheckboxSelectMultiple(
                                choices=tuple([a.id, a.name] for a in ChoicesMoVSource.objects.all().order_by('id')))
                    else:
                        self.fields['response'].widget = \
                            forms.widgets.Select(
                                choices=tuple([a.id, a.name] for a in ChoicesMoVSource.objects.all().order_by('id')))

                if self.instance.choices == MC1:
                    if self.instance.multi:
                        self.fields['response'].widget = \
                            forms.widgets.CheckboxSelectMultiple(choices=tuple([a.id, a.name] for a in
                            AssessmentChoicesMC1.objects.filter(assessment=self.instance.assessment).order_by('id')))
                    else:
                        self.fields['response'].widget = \
                            forms.widgets.Select(choices=tuple([a.id, a.name] for a in
                            AssessmentChoicesMC1.objects.filter(assessment=self.instance.assessment).order_by('id')))

                    # setting initial value with some processing of stored string of selected values
                    if self.instance.response:
                        selected = literal_eval(self.instance.response)
                        self.initial['response'] = selected

                    # add field to input new option
                    self.fields['other'] = forms.CharField(label=LABEL_TAG_ANY_OTHER, max_length=250, required=False)


                if self.instance.choices == MC2:
                    if self.instance.multi:
                        self.fields['response'].widget = \
                            forms.widgets.CheckboxSelectMultiple(
                                choices=tuple([a.id, a.name] for a in ChoicesMC2.objects.all().order_by('id')))
                    else:
                        self.fields['response'].widget = \
                            forms.widgets.Select(
                                choices=tuple([a.id, a.name] for a in ChoicesMC2.objects.all().order_by('id')))

                if self.instance.choices == SC1:
                    if self.instance.multi:
                        self.fields['response'].widget = \
                            forms.widgets.CheckboxSelectMultiple(
                                choices=tuple([a.id, a.name] for a in ChoicesSC1.objects.all().order_by('id')))
                    else:
                        self.fields['response'].widget = \
                            forms.widgets.Select(
                                choices=tuple([a.id, a.name] for a in ChoicesSC1.objects.all().order_by('id')))

                if self.instance.choices == SC2:
                    if self.instance.multi:
                        self.fields['response'].widget = \
                            forms.widgets.CheckboxSelectMultiple(choices=tuple([str(a.id), a.name]for a in
                            ChoicesSC2.objects.all().order_by('id')))
                    else:
                        self.fields['response'].widget = \
                            forms.widgets.Select(choices=tuple([str(a.id), a.name] for a in
                            ChoicesSC2.objects.all().order_by('id')))

                if self.instance.choices == SC3:
                    if self.instance.multi:
                        self.fields['response'].widget = \
                            forms.widgets.CheckboxSelectMultiple(
                                choices=tuple([a.id, a.name] for a in ChoicesSC3.objects.all().order_by('id')))
                    else:
                        self.fields['response'].widget = \
                            forms.widgets.Select(
                                choices=tuple([a.id, a.name] for a in ChoicesSC3.objects.all().order_by('id')))

                if self.instance.choices == SC4:
                    if self.instance.multi:
                        self.fields['response'].widget = \
                            forms.widgets.CheckboxSelectMultiple(
                                choices=tuple([a.id, a.name] for a in ChoicesSC4.objects.all().order_by('id')))
                    else:
                        self.fields['response'].widget = \
                            forms.widgets.Select(
                                choices=tuple([a.id, a.name] for a in ChoicesSC4.objects.all().order_by('id')))

                if self.instance.choices == SC5:
                    if self.instance.multi:
                        self.fields['response'].widget = \
                            forms.widgets.CheckboxSelectMultiple(
                                choices=tuple([a.id, a.name] for a in ChoicesSC5.objects.all().order_by('id')))
                    else:
                        self.fields['response'].widget = \
                            forms.widgets.Select(
                                choices=tuple([a.id, a.name] for a in ChoicesSC5.objects.all().order_by('id')))

            # add checkbox field for not applicable option
            """
            if self.instance.not_applicable:
                self.fields['n_a'] = forms.BooleanField(required=False, initial=False,
                                                        widget=forms.CheckboxInput(attrs={}))
            """
    class Meta:
        model = AssessmentComponentQuestion
        fields = '__all__'


class AssessmentHazardTypeForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(AssessmentHazardTypeForm, self).__init__(*args, **kwargs)

        # set multi and choices
        if self.instance:
            self.fields['r_a_year'].label = 'Year'
            self.fields['c_p_year'].label = 'Year'
            self.fields['risk_assessment'].label = 'Availability of specific risk assessment(s):'
            self.fields['contingency_plan'].label = 'Availability of specific contingency plan(s):'
            self.fields['subtypes'].label = 'Please select relevant hazard subtypes if applicable:'
            self.fields['subtypes'].widget = \
                forms.widgets.CheckboxSelectMultiple(
                    choices=tuple([a.id, a.h_subtype.name] for a in
                                  AssessmentHazardSubtype.objects.filter(a_h_type=self.instance).order_by('id')))

    class Meta:
        model = AssessmentHazardType
        fields = '__all__'