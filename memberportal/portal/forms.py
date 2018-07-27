from django import forms


class SpacebugForm(forms.Form):
        issue = forms.CharField(required=True)
        details = forms.CharField(
            required=True,
            widget=forms.Textarea
        )
