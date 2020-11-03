from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from accounts.models import Batch

class RegistrationForm(UserCreationForm):
    """docstring for ."""
    name = forms.CharField(label="Full Name",widget= forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter Your Full Name'}))
    email = forms.EmailField(label="Email Address",help_text="We'll never share your email with anyone else.", widget= forms.EmailInput(attrs={'class': 'form-control','aria-describedby':'emailHelp','placeholder':'Enter email'}))
    phone_number = forms.CharField(label="Phone Number",widget= forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter Your Phone Number'}))
    address = forms.CharField(label="Current Address",widget= forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter Your Current Address'}))
    password1 = forms.CharField(label="Password",help_text="Don't share your password with others",widget= forms.PasswordInput(attrs={'class': 'form-control','placeholder':'Enter Password'}))
    password2 = forms.CharField(label="Confirm Password",help_text="",widget= forms.PasswordInput(attrs={'class': 'form-control','placeholder':'Re-Enter Password'}))


    class Meta:
        """docstring for ."""
        model = get_user_model()
        fields = ('name','email','phone_number','address','password1','password2')


class Log_in_Form(forms.Form):
    """docstring for ."""
    email = forms.EmailField(label="Email Address",help_text="We'll never share your email with anyone else.", widget= forms.EmailInput(attrs={'class': 'form-control','aria-describedby':'emailHelp','placeholder':'Enter email'}))
    password = forms.CharField(label="Password",help_text="Don't share your password with others",widget= forms.PasswordInput(attrs={'class': 'form-control','placeholder':'Enter Password'}))
    class Meta:
        """docstring for ."""
        model = get_user_model()
        fields = ('email','password')

        def clean(self):
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email,password=password):
                raise forms.ValidationError("Invalid login")

class addBatchForm(forms.ModelForm):
    name = forms.CharField(label="Batch Name",help_text="Batch name must be uniquie",widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter the Batch name'}))
    capacity = forms.IntegerField(label="Capacity of this batch", min_value = 1,widget=forms.NumberInput(attrs={'class': 'form-control','placeholder':'Enter the Batch Capacity'}))
    class Meta:
        model = Batch
        fields = ('name','capacity')
