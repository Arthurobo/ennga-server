from django.contrib import admin
from .models import (MarketSectorBulkData, MarketSector, Historical, 
                    HistoricalCategory, MarketSectorCategory, 
                    GeoPhysicalCategory,
                    GeoPhysicalData, MarketSectorSubCategory
                )


class ModelAdminPreventDelete(admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return False
    

admin.site.register(MarketSectorBulkData, ModelAdminPreventDelete)
admin.site.register(MarketSector, ModelAdminPreventDelete)
admin.site.register(Historical, ModelAdminPreventDelete)
admin.site.register(GeoPhysicalCategory, ModelAdminPreventDelete)
admin.site.register(HistoricalCategory, ModelAdminPreventDelete)
admin.site.register(GeoPhysicalData, ModelAdminPreventDelete)
admin.site.register(MarketSectorCategory, ModelAdminPreventDelete)
admin.site.register(MarketSectorSubCategory, ModelAdminPreventDelete)