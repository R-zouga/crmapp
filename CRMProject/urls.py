from django.contrib import admin
from django.urls import path, include
from django.conf import settings

from CRMProject import baseviews

urlpatterns = [

    path("", baseviews.IndexView.as_view(), name="index"),
    path("<str:current_status>/history", baseviews.HistoryView.as_view(), name="history"),
    path("Service/", include("Service.urls")),
    path("Salesman/", include("Salesman.urls")),
    path("Supervisor/", include("Supervisor.urls")),
    path("Manager/", include("Manager.urls")),
    path("Client/", include("Client.urls")),
    path("Representative/", include("Representative.urls")),
    path("admin/", admin.site.urls),
    path("accounts/", include("User.urls")),
]

# make sure to include the "django_debug_urls" in development mode.
if settings.DEBUG:
    from debug_toolbar.toolbar import debug_toolbar_urls

    urlpatterns += debug_toolbar_urls()
