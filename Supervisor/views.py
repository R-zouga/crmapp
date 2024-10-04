import calendar

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch, Sum
from django.db.models.functions import ExtractMonth
from django.views.generic import TemplateView

from Salesman.models import Deal
from User.models import User, UserHistory
from django.utils.timezone import now


class SupervisorDashboard(LoginRequiredMixin, TemplateView):
    template_name = "supervisor/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["supervisor"] = User.objects.select_related(
            "supervisor__branch_group__group"
        ).get(email=self.request.user.email)
        context["salesmen"] = (
            context["supervisor"]
            .supervisor.branch_group.salesmen_set.select_related("user")
            .prefetch_related(
                Prefetch(
                    "user__userhistory_set",
                    queryset=UserHistory.objects.filter(
                        belonging_to__name=context["supervisor"].supervisor.branch_group
                    )
                    .order_by("user", "-join_date")
                    .distinct("user"),
                    to_attr="latest_record",
                )
            )
        )

        earnings_by_month = (
            Deal.objects.filter(
                time_of_state__year=now().year,
                attributed_to=self.request.user.supervisor.branch_group,
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

