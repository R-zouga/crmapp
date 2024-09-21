from django.views.generic import TemplateView
from User.models import UserHistory


class IndexView(TemplateView):
    template_name = "basiccomponents/index.html"


class HistoryView(TemplateView):
    template_name = "customcomponents/history.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["userhistory"] = UserHistory.objects.filter(
            user=self.request.user
        ).select_related("belonging_to", "responsible_for")
        context["template"] = f"{self.request.user.current_status}/dashboard.html"
        return context
