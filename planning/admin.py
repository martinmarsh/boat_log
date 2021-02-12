from django.contrib import admin
from planning.models import Plan, PlanPoint, TideRatePoint, TideStation, TideRate, WayPoint, TideHeightPoint
from boat_log.plan_actions import copy_plan


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ['title', 'active', 'start_from', 'to', 'start_time', 'end_time', 'distance', 'dtw', 'updated_at']
    ordering = ['title']
    list_filter = ['start_from']
    actions = ['reverse', 'append', 'copy', 'calculate']

    def append(self, request, queryset):
        pass

    def copy(self, request, queryset):
        for rec in queryset.iterator():
            copy_plan(rec)

    def reverse(self, request, queryset):
        pass

    def calculate(self, request, queryset):
        pass

    append.short_description = "Append to active route"
    reverse.short_description = "Reverse route"
    calculate.short_description = "Calculate"
    copy.short_description = "Copy"


@admin.register(PlanPoint)
class PlanPointAdmin(admin.ModelAdmin):
    list_display = ['number', 'name', 'description', 'cts', 'distance', 'set', 'drift',
                    'time', 'symbol', 'plan', 'way_point', 'updated_at']
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
