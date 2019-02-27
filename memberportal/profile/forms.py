from .models import Profile
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.forms.widgets import ClearableFileInput

User = get_user_model()


class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        max_length=254, required=True,
        help_text='We will never share your email with anyone without asking '
                  'you first.')
    password2 = forms.CharField(
        label='Confirm password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email',)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("Sorry, that email is already in use.")
        return email

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2


class AddProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'phone', 'screen_name',
                  'member_type', 'causes')

    def clean(self):
        causes = self.cleaned_data.get('causes')
        if causes and causes.count() > 3:
            raise ValidationError('Sorry, only three causes are allowed.')

        return self.cleaned_data


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'phone', 'screen_name', 'causes')

    def clean(self):
        causes = self.cleaned_data.get('causes')
        if causes and causes.count() > 3:
            raise ValidationError('Sorry, only three causes are allowed.')

        return self.cleaned_data


class AdminEditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('rfid', 'first_name', 'last_name', 'phone', 'member_type', 'screen_name', 'causes')

    def clean(self):
        causes = self.cleaned_data.get('causes')
        if causes and causes.count() > 3:
            raise ValidationError('Sorry, only three causes are allowed.')

        return self.cleaned_data


class AdminEditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'staff')


class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email',)


class ThemeFileInput(ClearableFileInput):
    template_name = 'theme_input.html'


class ThemeForm(forms.ModelForm):
    theme = forms.FileField(widget=ThemeFileInput, required=False)

    class Meta:
        model = Profile
        fields = ('theme',)


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


class StarvingHackerForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('studying_fulltime', 'centrelink', 'healthcare_card', 'income_bracket', 'special_consideration',
                  'special_consideration_note')
