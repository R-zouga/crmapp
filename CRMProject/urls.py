from django.contrib import admin
from django.urls import path, include
from django.conf import settings


urlpatterns = [
    path("", include("service.urls")),
    path("admin/", admin.site.urls),
    path("accounts/", include("user.urls")),
]

# make sure to include the "django_debug_urls" in development mode.
if settings.DEBUG:
    from debug_toolbar.toolbar import debug_toolbar_urls

    urlpatterns += debug_toolbar_urls()
