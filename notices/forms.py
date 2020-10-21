from django import forms
from accounts.models import Batch
from notices.models import Notice
from django.forms import ModelChoiceField


class add_notice_form(forms.ModelForm):
    notice = forms.CharField(label="Notice",max_length = 200, widget = forms.TextInput(attrs={'class':'form-control','placeholder':"Enter a Notice"}))
    batch = forms.ModelChoiceField(label="Select a batch", required=False,queryset=Batch.objects.all(),empty_label="All",widget = forms.Select(attrs={'class':'form-control','placeholder':"Select a Batch"}))
    class Meta:
        """docstring for ."""
        model = Notice
        fields = ('notice','batch')
