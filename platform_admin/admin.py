from django.contrib import admin
from .models import MarketSectorBulkData, MarketSector, Historical, GeoPoliticalData, HistoricalCategory, GeoPoliticalCategory, MarketSectorCategory

admin.site.register(MarketSectorBulkData)
admin.site.register(MarketSector)
admin.site.register(Historical)
admin.site.register(GeoPoliticalData)
admin.site.register(HistoricalCategory)
admin.site.register(GeoPoliticalCategory)
admin.site.register(MarketSectorCategory)