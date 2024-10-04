from Representative import views
from django.urls import path
urlpatterns = [
    path("dashboard/", views.RepresentativeDashboard.as_view(), name="dashboard"),
]