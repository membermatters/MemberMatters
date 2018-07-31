from django import forms
from .models import *


class DoorForm(forms.ModelForm):
    class Meta:
        model = Doors
        fields = ['name', 'description', 'ip_address', 'all_members']


class InterlockForm(forms.ModelForm):
    class Meta:
        model = Interlock
        fields = ['name', 'description', 'ip_address', 'all_members']
