from django.contrib import admin
from planning.models import Plan, PlanPoint


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    pass


@admin.register(PlanPoint)
class PlanPointAdmin(admin.ModelAdmin):
    pass
