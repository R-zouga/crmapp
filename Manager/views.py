from django.db.models import Prefetch
from django.views.generic import TemplateView
from User.models import User, UserHistory


class ManagerDashboard(TemplateView):
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
        return context
