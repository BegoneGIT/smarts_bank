from django.contrib import admin
from .models import Smart
# admin.site.register(Smart)

from django.apps import apps

# https://hackernoon.com/automatically-register-all-models-in-django-admin-django-tips-481382cf75e5
# for basic projects it should be ok

@admin.register(Smart)
class AdminSmart(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["project_name"]}


models = apps.get_models()

for model in models:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass