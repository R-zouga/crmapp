from django import forms
from django.core.exceptions import ValidationError

from User.models import User


class UserForm(forms.ModelForm):
    """A Custom User From for creating Client instances."""

    password = forms.CharField(
        widget=forms.PasswordInput(),
        label='Password'
    )
    password_confirmation = forms.CharField(
        widget=forms.PasswordInput(),
        label='Confirm Password'
    )

    def clean_password(self):
        """Further Validation method for password field."""
        password = self.cleaned_data.get('password')

        if len(password) < 8:
            raise ValidationError('Password must be at least 8 characters long.')

        if password.isdigit():
            raise ValidationError('Password cannot be entirely numeric.')

        return password

    def clean_password_confirmation(self):
        """Check that password confirmation is same as password."""
        password = self.cleaned_data.get('password')
        password_confirmation = self.cleaned_data.get('password_confirmation')

        if password and password_confirmation and password != password_confirmation:
            raise ValidationError('Passwords do not match.')

        return password_confirmation

    def clean_phone_number(self):
        """Make sure that number is all numeric."""
        phone_number = self.cleaned_data.get("phone_number")

        if not phone_number.isdigit():
            raise ValidationError("Phone number must contain only digits.")

        return phone_number

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "phone_number", "password")
        widgets = {"password": forms.PasswordInput()}
