from django import forms
from classlinks.models import Subject,Classtime,ClassLink
from django.core.exceptions import ValidationError
from accounts.models import Batch,User
from django.forms import ModelChoiceField
#

class assignTeacherChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return str(obj.id) + "  "+obj.name

class add_subject_form(forms.ModelForm):
    name = forms.CharField(label="Subject",max_length = 60, widget = forms.TextInput(attrs={'class':'form-control','placeholder':"Enter a subject name"}))
    batch = forms.ModelChoiceField(label="Select a batch",queryset=Batch.objects.all(), initial=0,widget = forms.Select(attrs={'class':'form-control','placeholder':"Select a Batch"}))
    teacher = assignTeacherChoiceField(label="Select a Teacher",queryset = User.objects.filter(is_teacher = True,teacher_aprove = True),initial=0,widget = forms.Select(attrs={'class':'form-control','placeholder':"Select a teacher"}))
    class Meta:
        """docstring for ."""
        model = Subject
        fields = ('name','batch','teacher')
#
#

class SubjectChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name + "( "+ obj.batch.name + " )"

class add_class_form(forms.ModelForm):
    """docstring for ."""
    teacher = forms.ModelChoiceField(label="Select a Teacher",queryset = User.objects.filter(is_teacher = True,teacher_aprove = True),initial=0,widget = forms.Select(attrs={'class':'form-control','placeholder':"Select a teacher"}))
    subject = SubjectChoiceField(label="Subject",queryset=Subject.objects.all(), initial=0,widget = forms.Select(attrs={'class':'form-control','placeholder':"Select a subject"}))
    classdate = forms.DateField(input_formats=['%d/%m/%Y'],widget=forms.DateInput(attrs={'class': 'form-control datetimepicker-input','data-target': '#datetimepicker1','placeholder':'Select a date'}))
    classtime = forms.ModelChoiceField(label="Time",queryset=Classtime.objects.all(), initial=0,widget = forms.Select(attrs={'class':'form-control','placeholder':"Select a tiem shedule"}))
    url = forms.URLField(widget = forms.URLInput(attrs={'class':'form-control','placeholder':"give class link heere"}))

    class Meta:
        """docstring for ."""
        model = ClassLink
        fields = ('teacher','subject','classdate','classtime','url')
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
