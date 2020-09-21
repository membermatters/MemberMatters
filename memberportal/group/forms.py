from django import forms
from .models import Group


class CauseForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ["name", "description", "item_code", "account_code"]
