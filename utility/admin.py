from django.contrib import admin

# Register your models here.
from .models import Country, State, City, GeoPoliticalZone, Clan

class ClanInline(admin.TabularInline):
    model = Clan

class CityInline(admin.TabularInline):
    model = City

class StateInline(admin.TabularInline):
    model = State


class CityAdmin(admin.ModelAdmin):
    inlines = [ClanInline]
    list_display = ('name', 'id')
    # list_editable = ('quiz',)


class StateAdmin(admin.ModelAdmin):
    inlines = [CityInline]
    list_display = ('name', 'id')
    # list_editable = ('quiz',)


class GeoPoliticalZoneAdmin(admin.ModelAdmin):
    inlines = [StateInline]
    list_display = ('name', 'id')
    # list_editable = ('quiz',)


admin.site.register(Country)
admin.site.register(GeoPoliticalZone, GeoPoliticalZoneAdmin)
admin.site.register(State, StateAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Clan)