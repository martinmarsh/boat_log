from django.contrib import admin
from planning.models import Plan, PlanPoint, TideRatePoint, TideStation, TideRates, WayPoint, TideHeightPoint


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


@admin.register(TideRates)
class TideRatesAdmin(admin.ModelAdmin):
    pass


@admin.register(WayPoint)
class WayPointAdmin(admin.ModelAdmin):
    pass
