from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import generics

from platform_admin.models import (
    MarketSector
)
from .serializers import (
    MarketSectorSerializer
)


class GeoPoliticalZoneListAPIView(generics.ListAPIView):
    queryset = MarketSector.objects.all()
    serializer_class = MarketSectorSerializer
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        geo_political_zone_id = self.kwargs.get('geo_political_zone_id')  # Extract geo_zone_id from URL
        return MarketSector.objects.filter(geo_political_zone_id=geo_political_zone_id)

class MarketSectorDetailAPIView(generics.RetrieveAPIView):
    queryset = MarketSector.objects.all()
    serializer_class = MarketSectorSerializer
    permission_classes = (permissions.AllowAny,)
    lookup_field = 'id'