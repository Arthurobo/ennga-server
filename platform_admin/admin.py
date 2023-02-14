from django.contrib import admin
from .models import MarketSectorBulkData, MarketSector, Historical, GeoPoliticalData

admin.site.register(MarketSectorBulkData)
admin.site.register(MarketSector)
admin.site.register(Historical)
admin.site.register(GeoPoliticalData)