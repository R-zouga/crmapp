from django.shortcuts import render
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = "base.html"


class EmployeeDashboard(TemplateView):
    template_name = "dashboards/employee-dashboard.html"


class SupervisorDashboard(TemplateView):
    template_name = "dashboards/supervisor-dashboard.html"
