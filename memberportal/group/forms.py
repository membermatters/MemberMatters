from django import forms
from .models import Group, CauseFund


class CauseForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ["name", "description", "item_code", "account_code"]


class CauseFundForm(forms.ModelForm):
    class Meta:
        model = CauseFund
        fields = ["name", "description", ]
