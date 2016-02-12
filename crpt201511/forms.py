from django.forms import ModelForm

import sys

from fields import *
from django import forms

from crpt201511.models import AssessmentCityIDQuestionUploadField, AssessmentCityIDQuestionFile, \
    AssessmentCityIDQuestionSelectField, MoVType
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


class AssessmentCityIDQuestionSelectFieldForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(AssessmentCityIDQuestionSelectFieldForm, self).__init__(*args, **kwargs)

        # set multi and choices
        if self.instance:

            if self.instance.choices and self.instance.choices.strip() <> "":
                if self.instance.multi:
                    self.fields['response'].widget = forms.SelectMultiple(choices=CHOICES[self.instance.choices])
                else:
                    self.fields['response'].widget = forms.Select(CHOICES[self.instance.choices])

            # add checkbox field for not applicable option
            if self.instance.not_applicable:
                self.fields['n_a'] = forms.BooleanField(required=False, initial=False,
                                                        widget=forms.CheckboxInput(attrs={}))


class AssessmentCityIDQuestionCharFieldForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(AssessmentCityIDQuestionCharFieldForm, self).__init__(*args, **kwargs)

        # add checkbox field for not applicable option
        if self.instance:
            if self.instance.not_applicable:
                self.fields['n_a'] = forms.BooleanField(required=False, initial=False, widget=forms.CheckboxInput(attrs={}))


class AssessmentCityIDQuestionTextFieldForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(AssessmentCityIDQuestionTextFieldForm, self).__init__(*args, **kwargs)

        # add checkbox field for not applicable option
        if self.instance:
            if self.instance.not_applicable:
                self.fields['n_a'] = forms.BooleanField(required=False, initial=False, widget=forms.CheckboxInput(attrs={}))

