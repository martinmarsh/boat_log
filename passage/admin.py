from django.contrib import admin
from passage.models import Passage, Position, SailLog, DepthLog, TideLog, FixLog, Track, TrackPoint
from .read_gpx_track import read_track

@admin.register(Passage)
class PassageAdmin(admin.ModelAdmin):
    pass


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    pass


@admin.register(SailLog)
class SailLogAdmin(admin.ModelAdmin):
    pass


@admin.register(DepthLog)
class DepthLogAdmin(admin.ModelAdmin):
    pass


@admin.register(TideLog)
class TideLogAdmin(admin.ModelAdmin):
    pass


@admin.register(FixLog)
class FixLogAdmin(admin.ModelAdmin):
    pass


def read_gpx_track(modeladmin, request, queryset):
    # queryset.update(status='p')
    for track in queryset.iterator():
        print(track.gpx_source_file)
        read_track(track.gpx_source_file, track)


read_gpx_track.short_description = "Read GPX and add to track"


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ['name', 'passage']
    ordering = ['name']
    actions = [read_gpx_track]


@admin.register(TrackPoint)
class TrackPointAdmin(admin.ModelAdmin):
    pass
