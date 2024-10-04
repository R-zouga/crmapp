from django.urls import path
from Manager import views
urlpatterns = [
    path("dashboard/", views.ManagerDashboard.as_view(), name="ManagerDashboard"),
    path("review-applicants/", views.ReviewApplicants.as_view(), name="review-applicants"),
    path("validate-record/<str:email>/", views.validate_record, name="validate-record"),
]
