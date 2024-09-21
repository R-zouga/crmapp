from django import forms
from Salesman.models import Meeting
class MeetingForm(forms.ModelForm):
    class Meta:
        model = Meeting
        fields = ['scheduled_time', 'google_meet_url']
        widgets = {
            'scheduled_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }