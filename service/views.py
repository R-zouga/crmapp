from django.shortcuts import render
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = "service/index.html"


def dashboard_view(request, current_status):
    return render(request, f"{current_status}/dashboard.html")
