from django import forms
from .models import Doors


class DoorForm(forms.ModelForm):
    class Meta:
        model = Doors
        fields = ['name', 'description', 'ip_address', 'all_members']
