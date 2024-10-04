from django.contrib import admin
from django.apps import apps

for app_config in apps.get_app_configs():
    for model in app_config.get_models():
        try:
            admin.site.register(model)
        except admin.sites.AlreadyRegistered:
            pass

admin.site.site_header = "CRM Project Administration"
admin.site.site_title = "CRM Admin Portal"
admin.site.index_title = "Welcome to the CRM Project Administration"

