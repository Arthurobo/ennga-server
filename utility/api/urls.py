from django.urls import path
from .views import (
    GeoPoliticalZoneListAPIView,
    StatesListAPIView
)

app_name = 'utility_api'

urlpatterns = [
    path('geo-political-zone-list-api-view/', GeoPoliticalZoneListAPIView.as_view(),),
    path('states-list-api-view/', StatesListAPIView.as_view(),),
]
