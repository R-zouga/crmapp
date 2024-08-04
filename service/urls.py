from django.urls import path

from service import views


urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("dashboard/salesman/", views.EmployeeDashboard.as_view(), name="salesman-dashboard"),
    path("dashboard/supervisor/", views.SupervisorDashboard.as_view(), name="supervisor-dashboard"),
]