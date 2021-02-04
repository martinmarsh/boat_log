from django.contrib import admin
from boat_log.models import WeatherLog, EngineLog, SeaLog


@admin.register(WeatherLog)
class WeatherLogAdmin(admin.ModelAdmin):
    pass


@admin.register(EngineLog)
class EngineLogAdmin(admin.ModelAdmin):
    pass


@admin.register(SeaLog)
class SeaLogAdmin(admin.ModelAdmin):
    pass
