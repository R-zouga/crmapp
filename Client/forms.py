from django import forms
from Service.models import Service
from Salesman.models import BranchGroup, Salesman


class ServiceForm(forms.ModelForm):
    salesman = forms.ModelChoiceField(queryset=Salesman.objects.all(), label='Salesman')
    branch = forms.ModelChoiceField(queryset=BranchGroup.objects.all(), label='Branch')

    class Meta:
        model = Service
        fields = ["name", "description", "price", "salesman", "branch"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['price'].widget = forms.TextInput(attrs={'type': 'text'})
