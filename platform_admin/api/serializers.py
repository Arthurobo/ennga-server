from rest_framework import serializers
from platform_admin.models import MarketSector

from utility.api.serializers import (
    CountrySerializer,
    TribeSerializer,
    GeoPoliticalZoneSerializer,
    StateSerializer,
    CitySerializer,
    ClanSerializer,
    SubClanSerializer
)


class MarketSectorSerializer(serializers.ModelSerializer):
    country = TribeSerializer(read_only=True)
    geo_political_zone = GeoPoliticalZoneSerializer(read_only=True)
    state = StateSerializer(read_only=True)
    city = CitySerializer(read_only=True)
    clan = ClanSerializer(read_only=True)
    subclan = SubClanSerializer(read_only=True)

    class Meta:
        model = MarketSector
        fields = "__all__"