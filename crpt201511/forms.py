from django.forms import ModelForm

from models import *
from constants import *
from fields import *


class AssessmentCityIDResponseForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(AssessmentCityIDResponseForm, self).__init__(*args, **kwargs)
        """
        if self.instance.value_type.name != UPLOAD_DOCS:
            self.fields['files'].widght = forms.HiddenInput()

        if self.instance.value_type.name == TEXT_FIELD:
                self.fields['value'].widget = forms.Textarea(attrs={'cols': 21, 'rows': 3})
        """
    files = MultiFileField(min_num=1, max_num=3, max_file_size=1024*1024*5)

    class Meta:
        model = AssessmentCityIDResponse
        exclude = []
