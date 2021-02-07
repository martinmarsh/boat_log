from django.contrib import admin
from planning.models import Plan, PlanPoint, TideRatePoint, TideStation, TideRate, WayPoint, TideHeightPoint


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    pass


@admin.register(PlanPoint)
class PlanPointAdmin(admin.ModelAdmin):
    pass


@admin.register(TideRatePoint)
class TideRatePointAdmin(admin.ModelAdmin):
    pass


@admin.register(TideStation)
class TideStationAdmin(admin.ModelAdmin):
    pass


@admin.register(TideHeightPoint)
class TideHeightPointAdmin(admin.ModelAdmin):
    pass


@admin.register(TideRate)
class TideRateAdmin(admin.ModelAdmin):
    pass


@admin.register(WayPoint)
class WayPointAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'time', 'type', 'symbol', 'updated_at']
    ordering = ['long']
