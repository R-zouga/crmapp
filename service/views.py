from django.db.models import Prefetch, Max
from django.shortcuts import render

from service.forms import StatusFilterForm
from user import models
from django.views.generic import TemplateView


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
            .supervisor.branch_group.salesman_set.select_related("user")
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
    template_name = "service/history.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["userhistory"] = models.UserHistory.objects.filter(
            user=self.request.user
        ).select_related("belonging_to", "responsible_for")
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


def salesman_dashbord(request):
    form = StatusFilterForm(request.GET or None)
    salesman = models.Salesman.objects.get(user=request.user)
    deals = salesman.deal_set.all().select_related("client__user", "attributed_to", "service")

    if form.is_valid():
        status = form.cleaned_data.get("status")
        if status:
            deals = salesman.deal_set.filter(status=status)

    if "HX-Request" in request.headers:
        return render(request, "salesman/deal_list_partial.html", {"deals": deals})

    return render(request, "salesman/deal_list.html", {"form": form, "deals": deals})
