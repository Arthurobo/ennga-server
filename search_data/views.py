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
from .serializers import (
    SearchDocumentSerializer, 
    SearchDataImportListSerializer,
    SearchDataImportSerializer,
    SearchDataBookmarkListSerializer,
    SearchDataBookmarkSerializer,
    )
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwner
from .models import (SearchDataHistory, 
                     SearchDataImport, 
                     SearchDataBookmark) 
from rest_framework.views import APIView
from rest_framework.response import Response

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
    def list(self, request, *args, **kwargs):
        search_query = request.query_params.get("search")
        user = request.user

        SearchDataHistory.objects.create(user=user, search_query=search_query)
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