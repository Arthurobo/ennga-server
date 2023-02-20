from django.contrib import admin
from .models import (MarketSectorBulkData, MarketSector, Historical, 
                    HistoricalCategory, MarketSectorCategory, 
                    GeoPhysicalCategory,
                    GeoPhysicalData,
                )

admin.site.register(MarketSectorBulkData)
admin.site.register(MarketSector)
admin.site.register(Historical)
admin.site.register(GeoPhysicalCategory)
admin.site.register(HistoricalCategory)
admin.site.register(GeoPhysicalData)
admin.site.register(MarketSectorCategory)