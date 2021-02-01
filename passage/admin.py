from django.contrib import admin
from passage.models import Passage, Position, SailLog


@admin.register(Passage)
class PassageAdmin(admin.ModelAdmin):
    pass


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    pass


@admin.register(SailLog)
class SailLogAdmin(admin.ModelAdmin):
    pass
