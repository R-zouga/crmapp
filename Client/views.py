from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Max, Subquery, OuterRef
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView

from Client.forms import ServiceForm
from Manager.models import Manager, AskUpgrade
from Salesman.models import Meeting, Deal
from django.utils.timezone import now

from Service.models import Service


class ClientDashboard(LoginRequiredMixin, TemplateView):
    template_name = "Client/dashboard.html"

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


class NewServiceView(LoginRequiredMixin, FormView):
    template_name = "Client/new_service.html"
    form_class = ServiceForm
    success_url = reverse_lazy("ClientDashboard")

    def form_valid(self, form):
        salesman = form.cleaned_data["salesman"]
        branch = form.cleaned_data["branch"]
        name = form.cleaned_data["name"]
        description = form.cleaned_data["description"]
        price = form.cleaned_data["price"]

        if salesman not in branch.salesmen_set.all():
            form.add_error('salesman', 'The selected salesman does not belong to the selected branch')
            return self.form_invalid(form)
        else:
            service = Service.objects.create(
                name=name,
                description=description,
                price=price
            )
            Deal.objects.create(
                salesman=salesman,
                service=service,
                attributed_to=branch,
                service_seeker=self.request.user,
                time_of_state=now(),
            )
            return super().form_valid(form)


class ServiceUpdate(LoginRequiredMixin, TemplateView):
    template_name = "client/services_update.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        subquery = (
            Deal.objects.filter(service_seeker=self.request.user)
            .values("service")
            .annotate(latest_status_date=Max("time_of_state"))
        )
        deals_with_latest_status = Deal.objects.filter(
            time_of_state=Subquery(
                subquery.filter(service=OuterRef("service")).values(
                    "latest_status_date"
                )
            ),
        ).select_related(
            "salesman__user", "attributed_to__group", "service"
        )
        context["services"] = deals_with_latest_status
        return context


class AskUpgradeView(LoginRequiredMixin, TemplateView):
    template_name ="Client/askupgrade.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["manager"] = Manager.objects.all().first()
        return context

    def post(self, request, *args, **kwargs):
        client = self.request.user.client
        context = self.get_context_data()

        AskUpgrade.objects.get_or_create(client=client, manager=context["manager"])

        return HttpResponseRedirect("/Client/dashboard/")
