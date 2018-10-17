from django import forms
from .models import Causes


class CauseForm(forms.ModelForm):
    class Meta:
        model = Causes
        fields = ['name', 'description', "item_code", "account_code"]
