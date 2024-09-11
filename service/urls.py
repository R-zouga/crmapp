from django.urls import path, include
from service import views

Salesman = [
    path("dashboard/", views.SalesmanDashboard.as_view(), name="SalesmanDashboard"),
]

Supervisor = [
    path("dashboard/", views.SupervisorDashboard.as_view(), name="SupervisorDashboard"),
]


Manager = [
    path("dashboard/", views.ManagerDashboard.as_view(), name="ManagerDashboard"),
]
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<str:current_status>/history", views.HistoryView.as_view(), name="history"),
    path("Salesman/", include(Salesman)),
    path("Supervisor/", include(Supervisor)),
    path("Manager/", include(Manager)),
]