from .models import *
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254, required=True,
                             help_text='We will never share your email with anyone without asking you first.')
    password1 = forms.CharField(label="Password",
                                widget=forms.PasswordInput,
                                help_text='You can\'t use something similar to your other info, or something too '
                                          'simple/common. The minimum length is 8 characters.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )


class AddProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('member_type', 'cause1', 'cause2', 'cause3')


class EditCausesForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('cause1', 'cause2', 'cause3')


class AdminEditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('member_type', 'rfid', 'cause1', 'cause2', 'cause3')


class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']


class CauseForm(forms.ModelForm):
    class Meta:
        model = Causes
        fields = ['name', 'description']


class DoorForm(forms.ModelForm):
    class Meta:
        model = Doors
        fields = ['name', 'description', 'all_members']
