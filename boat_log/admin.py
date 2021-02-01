from django.contrib import admin
from boat_log.models import WeatherLog, EngineLog


@admin.register(WeatherLog)
class WeatherLogAdmin(admin.ModelAdmin):
    pass


@admin.register(EngineLog)
class EngineLogAdmin(admin.ModelAdmin):
    pass
