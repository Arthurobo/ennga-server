from django_elasticsearch_dsl_drf.filter_backends import (
    FilteringFilterBackend,
    CompoundSearchFilterBackend,
)
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
from django_elasticsearch_dsl_drf.filter_backends import (
    FilteringFilterBackend,
    OrderingFilterBackend,
)
from rest_framework.permissions import IsAuthenticated

from .documents import SearchDocument
from .serializers import (
    SearchDocumentSerializer, 
    SearchDataImportListSerializer,
    SearchDataImportSerializer,
    SearchDataBookmarkListSerializer,
    SearchDataBookmarkSerializer,
    )
from rest_framework import generics
from .permissions import IsOwner
from .models import (SearchHistory, 
                     SearchDataImport, 
                     SearchDataBookmark) 
from rest_framework.views import APIView
from rest_framework.response import Response


class SearchDocumentView(DocumentViewSet):
    document = SearchDocument
    serializer_class = SearchDocumentSerializer
    # permission_classes = [IsAuthenticated]
    
    lookup_field = "title"
    fielddata = True
    filter_backends = [
        FilteringFilterBackend,
        OrderingFilterBackend,
        CompoundSearchFilterBackend,
    ]
    search_fields = ("title","description",)
    multi_match_search_fields = (
        "title",
        "description",
    )

    filter_fields = {}

    ordering_fields = {
        "id": None,
        "date_created": "date_created",
        "last_updated": "last_updated",
    }
    ordering = ("-date_created", "-last_updated")
    def list(self, request, *args, **kwargs):
        search_term = request.query_params.get("search")
        user = request.user

        SearchHistory.objects.create(user=user, search_term=search_term)
        return super().list(request, *args, **kwargs)


# List all imported data for a particular user
class SearchDataImportListAPIView(generics.ListAPIView):
    queryset = SearchDataImport.objects.all()
    serializer_class = SearchDataImportListSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        user = self.request.user.account_profile
        return super().get_queryset().filter(user=user).order_by("date_created")

# Import Data
class SearchDataImportAPIView(generics.CreateAPIView):
    queryset = SearchDataImport.objects.all()
    serializer_class = SearchDataImportSerializer
    permission_classes = [IsAuthenticated]

# List all BookMark data for a particular user
class SearchDataBookmarkListAPIView(generics.ListAPIView):
    queryset = SearchDataBookmark.objects.all()
    serializer_class = SearchDataBookmarkListSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        user = self.request.user.account_profile
        return super().get_queryset().filter(user=user).order_by("date_created")

# BookMark Data
class SearchDataBookmarkAPIView(generics.CreateAPIView):
    queryset = SearchDataBookmark.objects.all()
    serializer_class = SearchDataBookmarkSerializer
    permission_classes = [IsAuthenticated]
