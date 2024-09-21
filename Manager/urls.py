from django.urls import path
from Manager import views
urlpatterns = [
    path("dashboard/", views.ManagerDashboard.as_view(), name="ManagerDashboard"),
]
