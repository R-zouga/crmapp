import calendar

from django.db.models import Prefetch, Q, Sum, Max, F, OuterRef, Subquery
from django.db.models.functions import ExtractMonth
from django.shortcuts import render

from user import models
from django.views.generic import TemplateView
from django.utils.timezone import now

from datetime import date

import plotly.express as px


class IndexView(TemplateView):
    template_name = "service/index.html"


class SupervisorDashboard(TemplateView):
    template_name = "supervisor/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["supervisor"] = models.User.objects.select_related(
            "supervisor__branch_group__group"
        ).get(email=self.request.user.email)
        context["salesmen"] = (
            context["supervisor"]
            .supervisor.branch_group.salesmen_set.select_related("user")
            .prefetch_related(
                Prefetch(
                    "user__userhistory_set",
                    queryset=models.UserHistory.objects.filter(
                        belonging_to__name=context["supervisor"].supervisor.branch_group
                    )
                    .order_by("user", "-join_date")
                    .distinct("user"),
                    to_attr="latest_record",
                )
            )
        )
        return context


class HistoryView(TemplateView):
    template_name = f"service/history.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["userhistory"] = models.UserHistory.objects.filter(
            user=self.request.user
        ).select_related("belonging_to", "responsible_for")
        context["template"] = f"{self.request.user.current_status}/dashboard.html"
        return context


class ManagerDashboard(TemplateView):
    template_name = "manager/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["manager"] = models.User.objects.select_related(
            "manager__department__group"
        ).get(email=self.request.user.email)
        context["supervisors"] = (
            context["manager"]
            .manager.department.supervisor_set.select_related("user")
            .prefetch_related(
                Prefetch(
                    "user__userhistory_set",
                    queryset=models.UserHistory.objects.filter(
                        belonging_to__name=context["manager"].manager.department
                    )
                    .order_by("user", "-join_date")
                    .distinct("user"),
                    to_attr="latest_record",
                )
            )
        )
        return context


class SalesmanDashboard(TemplateView):
    template_name = "salesman/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["salesman"] = models.Salesman.objects.get(user=self.request.user)
        context["deals"] = (
            models.Deal.objects.filter(
                Q(status=models.Deal.Status.interested)
                | Q(status=models.Deal.Status.further_motivation),
                salesman=context["salesman"],
            )
            .exclude(status=models.Deal.Status.acquired)
            .select_related(
                "service_seeker", "attributed_to__group", "representing", "service"
            )
        )

        # Aggregating earnings by month for the current year
        earnings_by_month = (
            models.Deal.objects.filter(
                date_of_state__year=now().year, salesman=context["salesman"], status=100
            )
            .annotate(month=ExtractMonth("date_of_state"))
            .values("month")
            .annotate(total_earnings=Sum("service__price"))
            .order_by("month")
        )

        months = [calendar.month_name[entry["month"]] for entry in earnings_by_month]
        earnings = [entry["total_earnings"] for entry in earnings_by_month]
        fig = px.bar(
            x=months,
            y=earnings,
            labels={"x": "Month", "y": "Total Earnings"},  # Labels for axes
            text=earnings,
        )
        fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")

        # Generate HTML representation of the plot
        graph_html = fig.to_html(full_html=False, config={"displayModeBar": False})

        # Pass the chart and salesman to the template context
        context["earnings_graph"] = graph_html
        return context


class LostDeals(TemplateView):
    template_name = "salesman/lost_deals.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        subquery = (
            models.Deal.objects.filter(salesman=self.request.user.email)
            .values("service")
            .annotate(latest_status_date=Max("date_of_state"))
        )
        deals_with_latest_status = models.Deal.objects.filter(
            date_of_state=Subquery(
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
    record = models.Deal.objects.get(id=id)
    record.pk = None
    record.status = 2
    record.date_of_state = now()
    record.save()
    subquery = (
        models.Deal.objects.filter(salesman=request.user.email)
        .values("service")
        .annotate(latest_status_date=Max("date_of_state"))
    )
    deals_with_latest_status = models.Deal.objects.filter(
        date_of_state=Subquery(
            subquery.filter(service=OuterRef("service")).values(
                "latest_status_date"
            )
        ),
        status=-1,
    ).select_related(
        "service_seeker", "attributed_to__group", "representing", "service"
    )
    return render(request, "salesman/lost_deals_table.html", {"lost_deals": deals_with_latest_status})


class AppendedDeals(TemplateView):
    template_name = "salesman/appended_deals.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["appended_deals"] = models.Deal.objects.filter(
            salesman=self.request.user.email, status__in=[0, 2]
        ).select_related(
            "service_seeker", "attributed_to__group", "representing", "service"
        )
        return context


def meeting_review(request, id):
    record = models.Deal.objects.get(id=id)
    record.status = 1
    record.date_of_state = date.today
    record.save()
    context = {
        "appended_deals": (
            models.Deal.objects.filter(
                salesman=request.user.email, status__in=[0, 2]
            ).select_related(
                "service_seeker", "attributed_to__group", "representing", "service"
            )
        )
    }
    return render(request, "salesman/appended_deals_table.html", context)
