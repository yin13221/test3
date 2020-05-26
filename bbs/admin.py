from django.contrib import admin

# Register your models here.
from .models import Bbs


@admin.register(Bbs)
class BbsModelAdmin(admin.ModelAdmin):
    list_display = ("id", "subject", "content")

# admin.site.register(Bbs, BbsModelAdmin)
