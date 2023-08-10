import random

from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import generics

from utility.models import (
    GeoPoliticalZone,
    State
)
from .serializers import (
    GeoPoliticalZoneSerializer,
    StateSerializer
)


class GeoPoliticalZoneListAPIView(generics.ListAPIView):
    queryset = GeoPoliticalZone.objects.all()
    serializer_class = GeoPoliticalZoneSerializer
    permission_classes = (permissions.AllowAny,)


class StatesListAPIView(generics.ListAPIView):
    queryset = State.objects.all()
    serializer_class = StateSerializer
    permission_classes = (permissions.AllowAny,)