from django.db import models
from django.contrib import admin
from django.contrib.admin.sites import NotRegistered
from django.contrib.flatpages.admin import FlatPageAdmin as DjangoFlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from markdownx.widgets import AdminMarkdownxWidget


try:
    admin.site.unregister(FlatPage)
except NotRegistered:
    pass


@admin.register(FlatPage)
class FlatPageAdmin(DjangoFlatPageAdmin):
    list_display = ("__str__", "url", "title", "template_name")
    list_editable = ("url", "title")
    formfield_overrides = {models.TextField: {"widget": AdminMarkdownxWidget}}
