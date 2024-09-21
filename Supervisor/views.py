from django.db.models import Prefetch
from django.views.generic import TemplateView
from User.models import User, UserHistory

class SupervisorDashboard(TemplateView):
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
        return context
