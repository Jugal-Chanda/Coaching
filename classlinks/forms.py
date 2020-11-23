from django import forms
from classlinks.models import Subject,Classtime,ClassLink
from django.core.exceptions import ValidationError
from accounts.models import Batch,User
from django.forms import ModelChoiceField
#

class assignTeacherChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return str(obj.id) + "  "+obj.name




# class SubjectChoiceField(ModelChoiceField):
#     def label_from_instance(self, obj):
#         return obj.name + "( "+ obj.batch.name + " )"


#
class add_class_time_form(forms.ModelForm):
    starttime = forms.TimeField(label = "Select Start Time",input_formats = ['%H:%M'],widget=forms.TimeInput(attrs={'class': 'form-control datetimepicker-input','data-target': '#datetimepicker1'
    }))
    endtime = forms.TimeField(label = "Select End Time",input_formats = ['%H:%M'],widget=forms.TimeInput(attrs={'class': 'form-control datetimepicker-input','data-target': '#datetimepicker1'
    }))
    def clean(self):
        cleaned_data = super().clean()
        cc_starttime = cleaned_data.get("starttime")
        cc_endtime = cleaned_data.get("endtime")
        if cc_starttime >= cc_endtime:
            raise ValidationError(
                    "EndTime Must be grather than starttime"
                )
    class Meta:
        model = Classtime
        fields = ('starttime','endtime')
