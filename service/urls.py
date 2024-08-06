from django.urls import path

from service import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<str:current_status>/dashboard/", views.dashboard_view),
]