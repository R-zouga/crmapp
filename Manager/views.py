from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch, Sum
from django.db.models.functions import ExtractMonth
from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.list import ListView

from Client.models import Client
from Representative.models import Representative
from Salesman.models import Deal
from User.models import User, UserHistory
from Manager.models import AskUpgrade
from django.utils.timezone import now
import calendar
from datetime import date


class ManagerDashboard(LoginRequiredMixin, TemplateView):
    template_name = "manager/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["manager"] = User.objects.select_related(
            "manager__department__group"
        ).get(email=self.request.user.email)
        context["supervisors"] = (
            context["manager"]
            .manager.department.supervisor_set.select_related("user")
            .prefetch_related(
                Prefetch(
                    "user__userhistory_set",
                    queryset=UserHistory.objects.filter(
                        belonging_to__name=context["manager"].manager.department
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
                attributed_to__supervisor__in=self.request.user.manager.department.supervisor_set.all(),
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


class ReviewApplicants(LoginRequiredMixin, ListView):
    template_name = "manager/review.html"
    context_object_name = "reviews"

    def get_queryset(self):
        return AskUpgrade.objects.filter(manager=self.request.user.manager)


@login_required
def validate_record(request, email):
    user = User.objects.get(email=email)
    user.current_status = "Representative"
    user.save()
    record = AskUpgrade.objects.get(client=email)
    record.delete()

    record = Client.objects.get(user=email)
    record.delete()

    Representative.objects.create(user=user)

    record = UserHistory.objects.get(user=email, quit_date__isnull=True)
    record.quit_date = date.today()
    record.save()
    UserHistory.objects.create(user=user, join_date=date.today(), status="Representative")

    context = {"reviews": AskUpgrade.objects.filter(manager=request.user.manager)}
    return render(request, "manager/review_table.html", context)
