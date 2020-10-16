from django import forms
from classlinks.models import ClassLink
from vedios.models import Vedio


class ClasslinkChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.subject.batch.name + "-"+ obj.subject.name + "-" + str(obj.classdate)

class add_vedio_form(forms.ModelForm):
    """docstring for ."""
    classlink = ClasslinkChoiceField(label="Select a Class",queryset = ClassLink.objects.all(),initial=0,widget = forms.Select(attrs={'class':'form-control','placeholder':"Label Of this vedio"}))

    title = forms.CharField(label="Vedio Title",max_length = 60, widget = forms.TextInput(attrs={'class':'form-control','placeholder':"Enter a subject name"}))
    url = forms.URLField(label="Vedio Link",widget = forms.URLInput(attrs={'class':'form-control','placeholder':"Enter the vedio link here"}))

    class Meta:
        """docstring for ."""
        model = Vedio
        fields = ('classlink','title','url')
