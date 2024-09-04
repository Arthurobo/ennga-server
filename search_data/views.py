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
    SearchDataSerializer,
    )
from rest_framework import generics
from .permissions import IsOwner
from .models import SearchData, SearchHistory
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
class ImportDataListAPIView(generics.ListAPIView):
    queryset = SearchData.objects.all()
    serializer_class = SearchDataSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        user = self.request.user
        return super().get_queryset().filter(user_import=user)

# Import Data
class ImportDataAPIView(APIView):
    permission_classes = [IsAuthenticated, IsOwner]

    def put(self, request, *args, **kwargs):
        user = self.request.user
        search_data = self.kwargs["pk"]
        search_data = SearchData.objects.get(id=search_data)
        
        search_data.user_import.add(user)
        search_data.save()
        
        return Response({
            "search_data" : search_data.id,
            "user_id" : user.id
        })



# Remove imported data
class RemoveDataAPIView(APIView):
    permission_classes = [IsAuthenticated, IsOwner]

    def put(self, request, *args, **kwargs):
        user = self.request.user
        search_data = self.kwargs["pk"]
        search_data = SearchData.objects.filter(id=search_data,user=user)
        if search_data.exists() :
            search_data = search_data[0]
            search_data.user_import.remove(user)
            search_data.save()
            
            return Response({
            "search_data" : search_data.id,
            "user_id" : user.id
            }) 
        
        return Response({})

