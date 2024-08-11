from django.urls import path, include

from service import views

Supervisor = [
    path("dashboard/", views.SupervisorDashboard.as_view(), name="SupervisorDashboard"),
]
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<str:current_status>/history", views.HistoryView.as_view(), name="history"),
    path("Supervisor/", include(Supervisor)),
]