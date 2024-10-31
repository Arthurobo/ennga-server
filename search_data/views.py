from django_elasticsearch_dsl_drf.filter_backends import (
    FilteringFilterBackend,
    CompoundSearchFilterBackend,
)
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
from django_elasticsearch_dsl_drf.filter_backends import (
    FilteringFilterBackend,
    OrderingFilterBackend,
)
from rest_framework import permissions
from rest_framework.views import APIView
from .models import SearchDataHistory
from .documents import SearchDocument
from .serializers import SearchDocumentSerializer
from accounts.models import Profile
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



class SearchTotalListAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, *args, **kwargs):
        user = request.user
        profile = Profile.objects.get(user=user)
        total_searches = SearchDataHistory.objects.filter(user=profile).count()
        return Response({
            "user" : user.id,
            "total_searches" : total_searches
        })