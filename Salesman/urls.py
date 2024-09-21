from django.urls import path
from Salesman import views
urlpatterns = [
    path("dashboard/", views.SalesmanDashboard.as_view(), name="SalesmanDashboard"),
    path("lost-deals", views.LostDeals.as_view(), name="lost-deals"),
    path(
        "further-motivation/<int:id>",
        views.further_motivation,
        name="further-motivation",
    ),
    path("appended-deals", views.AppendedDeals.as_view(), name="appended-deals"),
    path("meeting-review/<int:id>", views.meeting_review, name="meeting-review"),
    path("waits-meeting", views.WaitsMeetingView.as_view(), name="waits-meeting"),
    path("set-meeting/<int:id>", views.SetMeetingView.as_view(), name="set-meeting"),
    path("confirm-meeting-result", views.MeetingResultView.as_view(), name="confirm-meeting-result"),

]
