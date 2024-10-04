from django.urls import path

from Client import views

urlpatterns = [
    path("dashboard/", views.ClientDashboard.as_view(), name="ClientDashboard"),
    path("new-service/", views.NewServiceView.as_view(), name="NewService"),
    path("servivce-updates/", views.ServiceUpdate.as_view(), name="ServiceUpdate"),
    path("upgrade-status/", views.AskUpgradeView.as_view(), name="ask-upgrade"),
]