from django.contrib import admin
from passage.models import Passage, Position, SailLog, DepthLog, TideLog, FixLog, Track, TrackPoint


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


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'passage']
    ordering = ['name']


@admin.register(TrackPoint)
class TrackPointAdmin(admin.ModelAdmin):
    list_display = ['id', 'track', 'number', 'segment', 'seg_num']
    ordering = ['track', 'number']
