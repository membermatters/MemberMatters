from .models import Profile
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(
        max_length=254, required=True,
        help_text='We will never share your email with anyone without asking '
                  'you first.')
    password1 = forms.CharField(
        label="Password", widget=forms.PasswordInput,
        help_text='The minimum length is 8 characters and you must include at '
                  'least one capital letter, number and special character.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',
                  'email', 'password1', 'password2',)


class AddProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('member_type', 'causes')

    def clean(self):
        causes = self.cleaned_data.get('causes')
        if causes and causes.count() > 3:
            raise ValidationError('Error, only three causes are allowed.')

        return self.cleaned_data


class AdminEditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('member_type', 'rfid', 'causes')

    def clean(self):
        causes = self.cleaned_data.get('causes')
        if causes and causes.count() > 3:
            raise ValidationError('Error, only three causes are allowed.')

        return self.cleaned_data


class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']


class ResetPasswordRequestForm(forms.Form):
    email = forms.CharField(required=True)


class ResetPasswordForm(forms.Form):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput,
        help_text='The minimum length is 8 characters and you must include at '
                  'least one capital letter, number and special character.')
    password2 = forms.CharField(label="Confirm Password",
                                widget=forms.PasswordInput)

    class Meta:
        fields = ['password1', 'password2']


class EditCausesForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('causes',)

    def clean(self):
        causes = self.cleaned_data.get('causes')
        if causes and causes.count() > 3:
            raise ValidationError('Error, only three causes are allowed.')

        return self.cleaned_data
