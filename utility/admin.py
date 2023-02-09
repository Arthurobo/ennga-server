from django.contrib import admin

# Register your models here.
from .models import Country, State, City

class CityInline(admin.TabularInline):
    model = City


class StateAdmin(admin.ModelAdmin):
    inlines = [CityInline]
    list_display = ('name', 'id')
    # list_editable = ('quiz',)


admin.site.register(Country)
admin.site.register(State, StateAdmin)
admin.site.register(City)