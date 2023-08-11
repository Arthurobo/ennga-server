from django.urls import path
from .views import GeoPoliticalZoneListAPIView, MarketSectorDetailAPIView

app_name = "platform_admin_api"

urlpatterns = [
    path('market-sectors/geo-zone/<int:geo_political_zone_id>/', GeoPoliticalZoneListAPIView.as_view(), name='geo-zone-market-sectors'),
    path('market-sectors/detail/<int:id>/', MarketSectorDetailAPIView.as_view(), name='market-sector-detail'),
]
