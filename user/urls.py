from django.urls import path

from user import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
