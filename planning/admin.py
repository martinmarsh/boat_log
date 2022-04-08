from django.contrib import admin
from planning.models import Plan, PlanPoint, TideRatePoint, TideStation, TideRate, WayPoint, TideHeightPoint, TideTimes
from boat_log.plan_actions import copy_plan, reverse_copy_plan, plan_route, copy_tide_rate
import datetime


def create_model_admin(model_admin, model, name=None):
    class Meta:
        proxy = True
        app_label = model._meta.app_label

    attrs = {'__module__': '', 'Meta': Meta}

    new_model = type(name, (model,), attrs)

    admin.site.register(new_model, model_admin)
    return model_admin


def last_updated(obj):
    return obj.updated_at.strftime("%a %y-%m-%d  %H:%M")


def start_time(obj):
    if obj.start_time:
        return obj.start_time.strftime("%a %y-%m-%d  %H:%M")
    return ""


def end_time(obj):
    if obj.end_time:
        return obj.end_time.strftime("%a %y-%m-%d  %H:%M")
    return ""


def passage_time(obj):
    if obj.end_time and obj.start_time:
        delta_time = obj.end_time - obj.start_time
        return round(delta_time.total_seconds()/3600.0, 1)
    return ""


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ['title', 'active', 'start_from', 'to', start_time, end_time, passage_time,
                    'distance', 'dtw', last_updated]
    ordering = ['title']
    list_filter = ['start_from', 'to']
    actions = ['reverse', 'copy', 'calculate']

    def append(self, request, queryset):
        pass

    def copy(self, request, queryset):
        for rec in queryset.iterator():
            copy_plan(rec)

    def reverse(self, request, queryset):
        for rec in queryset.iterator():
            reverse_copy_plan(rec)

    def calculate(self, request, queryset):
        for rec in queryset.iterator():
            plan_route(rec)

    append.short_description = "Append to active route"
    reverse.short_description = "Reverse copy"
    calculate.short_description = "Calculate"
    copy.short_description = "Copy"


@admin.register(PlanPoint)
class PlanPointAdmin(admin.ModelAdmin):
    list_display = ['number', 'fixed', 'name', 'major', 'description', 'cts', 'cog',  'distance', 'dtw', 'set', 'drift',
                    'time_display', 'symbol', 'lat', 'long', last_updated, 'way_point', 'plan']
    ordering = ['plan', 'number']
    list_filter = ['plan', 'fixed', 'major']

    _last_date_display = datetime.datetime.now()

    def time_display(self, obj):
        if int(obj.number) == 1 or self._last_date_display.date() != obj.time.date():
            fmt = "%a %d %b %y  %H:%M"
            self._last_date_display = obj.time
        else:
            fmt = "%H:%M"
        return obj.time.strftime(fmt)

    time_display.short_description = 'Date/ETA'


class TideRatePointInline(admin.TabularInline):
    model = TideRatePoint


@admin.register(TideRate)
class TideRateAdmin(admin.ModelAdmin):
    list_display = ['name', 'tide_station', 'channel_flow', 'lat', 'long']
    ordering = ['name']
    inlines = [TideRatePointInline]
    fields = (('name', 'tide_station'), ('channel_flow', 'lat', 'long'))
    list_filter = ['tide_station']
    actions = ['copy']

    def copy(self, request, queryset):
        for rec in queryset.iterator():
            copy_tide_rate(rec)


class TideTimesInline(admin.TabularInline):
    model = TideTimes


@admin.register(TideStation)
class TideStationAdmin(admin.ModelAdmin):
    inlines = [TideTimesInline]


@admin.register(TideHeightPoint)
class TideHeightPointAdmin(admin.ModelAdmin):
    list_display = ['hrs', 'spring', 'neap', 'tide_station']
    ordering = ['hrs']
    list_filter = ['tide_station']


@admin.register(WayPoint)
class WayPointAdmin(admin.ModelAdmin):
    list_display = ['name', 'active', 'description','time', 'type', 'symbol', 'lat', 'long', 'updated_at']
    ordering = ['long']
    list_filter = ['symbol', 'psym', 'type', 'tide_station', 'tide_rates']
    actions = ['activate', 'deactivate']

    def activate(self, request, queryset):
        for rec in queryset.iterator():
            rec.active = True
            rec.save()

    def deactivate(self, request, queryset):
        for rec in queryset.iterator():
            rec.active = False
            rec.save()
    
    activate.short_description = "make active"
    deactivate.short_description = "deactivate"


class PlanPointInline(admin.TabularInline):
    model = PlanPoint
    readonly_fields = ['number', 'fixed', 'name', 'major', 'description', 'cts',
                       'cog', 'distance', 'dtw', 'smg', 'set', 'drift',
                        'time_display',  'lat', 'long', last_updated]

    exclude = ['time', 'symbol', 'psym', 'extensions', 'opencpn_extensions', 'opencpn_guid', 'links', 'type',
               'arrival_radius', 'tide_rates', 'way_point']
    ordering = ['number']

    _last_date_display = datetime.datetime.now()

    def time_display(self, obj):
        if self._last_date_display.date() != obj.time.date():
            fmt = "%a %d %b %y  %H:%M"
            self._last_date_display = obj.time
        else:
            fmt = "%H:%M"
        return obj.time.strftime(fmt)

    time_display.short_description = 'Date/ETA'


class PlanShowAdmin(admin.ModelAdmin):
    list_display = ['title', 'active', 'start_from', 'to', start_time, end_time, passage_time,
                    'distance', 'dtw', last_updated]
    fields = (('active', 'title', 'plan_speed', 'start_time'),
              ('start_from', 'to', passage_time),
              ('end_time', 'distance', 'dtw'))
    inlines = [PlanPointInline]
    readonly_fields = ['start_from', 'to', 'end_time', passage_time, 'distance',
                       'dtw', last_updated]

    exclude = ['extensions', 'opencpn_extensions', 'opencpn_guid', 'wind_force',
               'wind_direction', 'notes', 'becoming_wind_force', 'becoming_direction']

    ordering = ['title']
    list_filter = ['start_from', 'to']
    actions = ['reverse', 'copy', 'calculate']

    def append(self, request, queryset):
        pass

    def copy(self, request, queryset):
        for rec in queryset.iterator():
            copy_plan(rec)

    def reverse(self, request, queryset):
        for rec in queryset.iterator():
            reverse_copy_plan(rec)

    def calculate(self, request, queryset):
        for rec in queryset.iterator():
            plan_route(rec)

    append.short_description = "Append to active route"
    reverse.short_description = "Reverse copy"
    calculate.short_description = "Calculate"
    copy.short_description = "Copy"


create_model_admin(PlanShowAdmin, name='view-plan', model=Plan)
