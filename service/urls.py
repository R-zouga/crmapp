from django.urls import path, include
from service import views

Salesman = [
    path("dashboard/", views.SalesmanDashboard.as_view(), name="SalesmanDashboard"),
    path("lost-deals", views.LostDeals.as_view(), name="lost-deals"),
    path("further-motivation/<int:id>", views.further_motivation, name="further-motivation"),
    path("appended-deals", views.AppendedDeals.as_view(), name="appended-deal"),
    path("appended-deal/<int:id>", views.meeting_review, name="meeting-review"),
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