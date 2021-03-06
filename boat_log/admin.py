from django.contrib import admin
from boat_log.models import WeatherLog, EngineLog, SeaLog, ExchangeLocation, GPXReadFile, GPXWriteFile
from .read_gpx import read_in
from .write_gpx import write_out
from datetime import datetime
from django.db.models import Q


@admin.register(WeatherLog)
class WeatherLogAdmin(admin.ModelAdmin):
    pass


@admin.register(EngineLog)
class EngineLogAdmin(admin.ModelAdmin):
    pass


@admin.register(SeaLog)
class SeaLogAdmin(admin.ModelAdmin):
    pass


@admin.register(ExchangeLocation)
class ExchangeLocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'directory']
    ordering = ['name']


@admin.register(GPXReadFile)
class GPXReadFileAdmin(admin.ModelAdmin):
    list_display = ['gpx_file_name', 'directory', 'write_time']
    ordering = ['gpx_file_name']
    actions = ['read_gpx']

    def read_gpx(self, request, queryset):
        for rec in queryset.iterator():
            try:
                read_in(rec.directory.directory, rec.gpx_file_name)
                rec.write_time = datetime.now()
                rec.save()
            except Exception as e:
                raise e

    read_gpx.short_description = "Read GPX into all tables"


@admin.register(GPXWriteFile)
class GPXWriteFileAdmin(admin.ModelAdmin):
    list_display = ['gpx_file_name', 'directory', 'from_date', 'write_time']
    ordering = ['gpx_file_name']
    actions = ['write_gpx_date', 'write_gpx_active']

    def write_gpx_date(self, request, queryset):
        for rec in queryset.iterator():
            select = Q(updated_at__gte=rec.from_date)
            self.write_gpx(rec, select)

    def write_gpx_active(self, request, queryset):
        for rec in queryset.iterator():
            select = Q(active=True)
            self.write_gpx(rec, select)

    def write_gpx(self, rec, select):
        write_out(rec.directory.directory, rec.gpx_file_name, select, rec.content, rec.extensions)
        rec.write_time = datetime.now()
        rec.save()

    write_gpx_date.short_description = "Write updated records to GPX file"
    write_gpx_active.short_description = "Write active records to GPX file"


