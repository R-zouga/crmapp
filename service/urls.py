from django.urls import path

from service import views

app_name = "SimplyRecipes"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
]