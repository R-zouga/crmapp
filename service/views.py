from user import models
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = "service/index.html"


class SupervisorDashboard(TemplateView):
    template_name = "supervisor/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["supervisor"] = self.request.user.supervisor
        context["group"] = context["supervisor"].branch_group.salesman_set.select_related("user")
        return context


class HistoryView(TemplateView):
    template_name = "service/history.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["userhistory"] = models.UserHistory.objects.filter(user=self.request.user)
        return context
