from django.db.models import Sum, Max, Subquery, OuterRef, Q
from django.db.models.functions import ExtractMonth
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.views.generic import TemplateView
from Salesman.models import Salesman, Deal, Meeting
from django.utils.timezone import now
import calendar
from datetime import date
from django.views.generic.edit import FormView
from django.core.mail import send_mail
from Salesman.forms import MeetingForm


class SalesmanDashboard(TemplateView):
    template_name = "Salesman/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["upcoming_meetings"] = Meeting.objects.filter(
            deal_id__salesman__user=self.request.user, scheduled_time__gt=now()
        ).select_related("deal_id__service_seeker")

        earnings_by_month = (
            Deal.objects.filter(
                time_of_state__year=now().year,
                salesman=Salesman.objects.get(user=self.request.user),
                status=100,
            )
            .annotate(month=ExtractMonth("time_of_state"))
            .values("month")
            .annotate(total_earnings=Sum("service__price"))
            .order_by("month")
        )

        context["months"] = [
            calendar.month_name[entry["month"]] for entry in earnings_by_month
        ]
        context["earnings"] = [entry["total_earnings"] for entry in earnings_by_month]
        return context


class LostDeals(TemplateView):
    template_name = "salesman/lost_deals.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        subquery = (
            Deal.objects.filter(salesman=self.request.user.email)
            .values("service")
            .annotate(latest_status_date=Max("time_of_state"))
        )
        deals_with_latest_status = Deal.objects.filter(
            time_of_state=Subquery(
                subquery.filter(service=OuterRef("service")).values(
                    "latest_status_date"
                )
            ),
            status=-1,
        ).select_related(
            "service_seeker", "attributed_to__group", "representing", "service"
        )
        context["lost_deals"] = deals_with_latest_status
        return context


def further_motivation(request, id):
    record = Deal.objects.get(id=id)
    record.pk = None
    record.status = 2
    record.time_of_state = now()
    record.save()
    subquery = (
        Deal.objects.filter(salesman=request.user.email)
        .values("service")
        .annotate(latest_status_date=Max("time_of_state"))
    )
    deals_with_latest_status = Deal.objects.filter(
        time_of_state=Subquery(
            subquery.filter(service=OuterRef("service")).values("latest_status_date")
        ),
        status=-1,
    ).select_related(
        "service_seeker", "attributed_to__group", "representing", "service"
    )
    return render(
        request,
        "salesman/lost_deals_table.html",
        {"lost_deals": deals_with_latest_status},
    )


class AppendedDeals(TemplateView):
    template_name = "salesman/appended_deals.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        subquery = (
            Deal.objects.filter(salesman=self.request.user.email)
            .values("service")
            .annotate(latest_status_date=Max("time_of_state"))
        )
        deals_with_latest_status = Deal.objects.filter(
            time_of_state=Subquery(
                subquery.filter(service=OuterRef("service")).values(
                    "latest_status_date"
                )
            ),
            status__in=[0, 2],
        ).select_related(
            "service_seeker", "attributed_to__group", "representing", "service"
        )
        context["appended_deals"] = deals_with_latest_status
        return context


def meeting_review(request, id):
    record = Deal.objects.get(id=id)
    record.pk = None
    record.status = 1
    record.time_of_state = now()
    record.save()
    subquery = (
        Deal.objects.filter(salesman=request.user.email)
        .values("service")
        .annotate(latest_status_date=Max("time_of_state"))
    )
    deals_with_latest_status = Deal.objects.filter(
        time_of_state=Subquery(
            subquery.filter(service=OuterRef("service")).values("latest_status_date")
        ),
        status__in=[0, 2],
    ).select_related(
        "service_seeker", "attributed_to__group", "representing", "service"
    )
    return render(
        request,
        "salesman/appended_deals_table.html",
        {"appended_deals": deals_with_latest_status},
    )


class WaitsMeetingView(TemplateView):
    template_name = "salesman/waits_meeting.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        subquery = (
            Deal.objects.filter(salesman=self.request.user.email)
            .values("service")
            .annotate(latest_status_date=Max("time_of_state"))
        )
        meeting_deals_subquery = Meeting.objects.values("deal_id")
        deals_with_latest_status = (
            Deal.objects.filter(
                time_of_state=Subquery(
                    subquery.filter(service=OuterRef("service")).values(
                        "latest_status_date"
                    )
                ),
                status=1,
            )
            .exclude(id__in=Subquery(meeting_deals_subquery))
            .select_related("service_seeker", "service")
        )
        context["deals_waiting_meeting"] = deals_with_latest_status
        return context


class SetMeetingView(FormView):
    template_name = "salesman/set_meeting.html"
    form_class = MeetingForm

    def dispatch(self, request, *args, **kwargs):
        self.deal = get_object_or_404(Deal, id=kwargs["id"])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["deal"] = self.deal
        occupied_meetings = Meeting.objects.filter(
            deal_id__salesman__user=self.request.user, scheduled_time__gt=now()
        )
        occupied_hours = [
            meeting.scheduled_time.strftime("%Y-%m-%dT%H")
            for meeting in occupied_meetings
        ]

        # Add occupied hours to the context
        context["occupied_hours"] = occupied_hours
        return context

    def form_valid(self, form):
        scheduled_time = form.cleaned_data["scheduled_time"]
        if scheduled_time <= now():
            form.add_error(
                "scheduled_time", "The scheduled time cannot be in the past."
            )
            return self.form_invalid(form)

        meeting = form.save(commit=False)
        meeting.deal_id = self.deal
        meeting.save()
        self.send_confirmation_email(meeting)
        return redirect("SalesmanDashboard")

    def send_confirmation_email(self, meeting):
        seeker_email = meeting.deal_id.service_seeker
        salesman_email = self.request.user.email
        seeker_message = render_to_string(
            "salesman/seeker_service_email.html", {"meeting": meeting}
        )
        seeker_subject = render_to_string("salesman/seeker_service_email.txt")

        salesman_message = render_to_string(
            "salesman/salesman_meeting_email.html", {"meeting": meeting}
        )
        salesman_subject = render_to_string("salesman/salesman_meeting_email.txt")
        send_mail(
            message="",
            subject=seeker_subject,
            from_email="noreply@crmproject.com",
            recipient_list=[seeker_email],
            html_message=seeker_message,
        )

        send_mail(
            message="",
            subject=salesman_subject,
            from_email="noreply@crmproject.com",
            recipient_list=[salesman_email],
            html_message=salesman_message,
        )


class MeetingResultView(TemplateView):
    pass
