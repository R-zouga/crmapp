from django.contrib.auth import views as auth_views, login
from django.shortcuts import redirect


class LoginView(auth_views.LoginView):
    def form_valid(self, form):
        """Security check complete. Log the user in."""
        user = form.get_user()
        login(self.request, user)
        return redirect(f"/{user.current_status}/dashboard/")


class PasswordResetView(auth_views.PasswordResetView):
    pass
