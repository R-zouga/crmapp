from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from Salesman.models import Meeting
from django.utils.timezone import now


class RepresentativeDashboard(LoginRequiredMixin, TemplateView):
    template_name = "representative/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["upcoming_meetings"] = Meeting.objects.filter(
            deal_id__service_seeker=self.request.user, scheduled_time__gt=now()
        ).select_related(
            "deal_id__representing",
            "deal_id__salesman",
            "deal_id__attributed_to__group",
            "deal_id__service",
        )
        return context