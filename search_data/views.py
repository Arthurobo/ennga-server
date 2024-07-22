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
from .serializers import SearchDocumentSerializer

class SearchDocumentView(DocumentViewSet):
    document = SearchDocument
    serializer_class = SearchDocumentSerializer
    permission_classes = [IsAuthenticated]
    
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
