from django.contrib.auth import views as auth_views, login
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import FormView
from user import models
from user.forms import UserForm
from django.db import transaction


class LoginView(auth_views.LoginView):
    def form_valid(self, form):
        """Security check complete. Log the user in and redirect him to his page based on his status."""
        user = form.get_user()
        login(self.request, user)
        return redirect(f"/{user.current_status}/dashboard/")


class CreateNewClient(SuccessMessageMixin, FormView):
    model = models.User
    form_class = UserForm
    template_name = "registration/new_account.html"
    success_url = reverse_lazy("index")
    success_message = "Congratulations on creating your new account."

    @transaction.atomic
    def form_valid(self, form):
        cleaned_data = form.cleaned_data
        user = models.User.objects.create_user(
            first_name=cleaned_data["first_name"],
            last_name=cleaned_data["last_name"],
            email=cleaned_data["email"],
            password=cleaned_data["password"],
            phone_number=cleaned_data["phone_number"],
            current_status="Client"
        )

        models.UserHistory.objects.create(user=user, status="Client")
        return super().form_valid(form)
