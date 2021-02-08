from django.contrib import admin
from planning.models import Plan, PlanPoint, TideRatePoint, TideStation, TideRate, WayPoint, TideHeightPoint


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ['title', 'start_from', 'to', 'start_time', 'end_time', 'distance', 'dtw', 'updated_at']
    ordering = ['title']
    list_filter = ['start_from']


@admin.register(PlanPoint)
class PlanPointAdmin(admin.ModelAdmin):
    list_display = ['plan', 'number', 'name', 'cts', 'time', 'symbol', 'way_point', 'updated_at']
    ordering = ['plan', 'number']
    list_filter = ['plan']


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
    list_filter = ['symbol', 'psym', 'type', 'tide_station', 'tide_rates']
