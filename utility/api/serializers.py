import random
import string
from rest_framework import serializers
from utility.models import (
    Country,
    Tribe,
    GeoPoliticalZone,
    State,
    City,
    Clan,
    SubClan
)

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = "__all__"


class TribeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tribe
        fields = "__all__"


class GeoPoliticalZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeoPoliticalZone
        fields = "__all__"


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = "__all__"


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = "__all__"


class ClanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clan
        fields = "__all__"


class SubClanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubClan
        fields = "__all__"
