from django.urls import path
from Supervisor import views
urlpatterns = [
    path("dashboard/", views.SupervisorDashboard.as_view(), name="SupervisorDashboard"),
]
