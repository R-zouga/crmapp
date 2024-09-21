from django import forms
from User.models import Deal


class StatusFilterForm(forms.Form):
    status = forms.ChoiceField(choices=Deal.Status.choices, required=False)
