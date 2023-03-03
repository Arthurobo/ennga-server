from django.contrib import admin

# Register your models here.
from .models import Country, State, City, GeoPoliticalZone, Clan, SubClan


class SubClanInline(admin.TabularInline):
    model = SubClan

class ClanInline(admin.TabularInline):
    model = Clan

class CityInline(admin.TabularInline):
    model = City

class StateInline(admin.TabularInline):
    model = State


class CityAdmin(admin.ModelAdmin):
    inlines = [ClanInline]
    list_display = ('name', 'id')
    search_fields = ['name',]
    # list_editable = ('quiz',)


class ClanAdmin(admin.ModelAdmin):
    inlines = [SubClanInline]
    list_display = ('name', 'id')
    search_fields = ['name',]
    # list_editable = ('quiz',)


class StateAdmin(admin.ModelAdmin):
    inlines = [CityInline]
    list_display = ('name', 'id')
    search_fields = ['name',]
    # list_editable = ('quiz',)


class GeoPoliticalZoneAdmin(admin.ModelAdmin):
    inlines = [StateInline]
    list_display = ('name', 'id')
    search_fields = ['name',]
    # list_editable = ('quiz',)

class SubClanAdmin(admin.ModelAdmin):
    search_fields = ['name',]


admin.site.register(Country)
admin.site.register(GeoPoliticalZone, GeoPoliticalZoneAdmin)
admin.site.register(State, StateAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Clan, ClanAdmin)
admin.site.register(SubClan, SubClanAdmin)