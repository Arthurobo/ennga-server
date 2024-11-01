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
from .models import SearchDataHistory, SearchData, SearchDataShare, SearchDataSaved, SearchDataUpload
from .documents import SearchDocument
from .serializers import (
    SearchDocumentSerializer, 
    SearchDataImportListSerializer,
    SearchDataImportSerializer,
    SearchDataBookmarkListSerializer,
    SearchDataBookmarkSerializer,
    SearchDataCreateSerializer,
    SearchDataUpdateSerializer,
    SearchDataDeleteSerializer,
    SearchDataShareSerializer,
    SearchDataUploadSerializer,
    SearchDataBookmarkDeleteSerializer,
    TopSearchSerializer,
    SearchDataSerializer
    )
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwner
from .models import (SearchDataHistory, 
                     SearchDataImport, 
                     SearchDataBookmark,
                     SearchDataUpload,
                     SearchDataHistory,
                     ) 
from rest_framework.views import APIView
from rest_framework.response import Response

from accounts.models import Profile
from rest_framework.response import Response
from .paginators.search_data_pagination import SearchDataPagination
from rest_framework.generics import CreateAPIView, UpdateAPIView
from django.db.models import Count
from rest_framework import status


class SearchDocumentView(DocumentViewSet):
    document = SearchDocument
    serializer_class = SearchDocumentSerializer
    pagination_class = SearchDataPagination
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
    def list(self, request, *args, **kwargs):
        search_query = request.query_params.get("search")
        user = request.user.account_profile

        SearchDataHistory.objects.create(user=user, search_query=search_query)
        return super().list(request, *args, **kwargs)
    

# Searchdata create endpoint

class SearchDataCreateAPIView(CreateAPIView):
    queryset = SearchData.objects.all()
    serializer_class = SearchDataCreateSerializer

# search data update
class SearchDataUpdateAPIView(UpdateAPIView):
    queryset = SearchData.objects.all()
    serializer_class = SearchDataUpdateSerializer
    

# search data retrieve
class SearchDataRetrieveAPIView(generics.RetrieveAPIView):
    queryset = SearchData.objects.all()
    serializer_class = SearchDataSerializer

# search data delete
class SearchDataDeleteAPIView(UpdateAPIView):
    queryset = SearchData.objects.all()
    serializer_class = SearchDataDeleteSerializer
    
    def perform_update(self, serializer):
        instance = serializer.save()
        instance.is_deleted = True
        instance.save()
    


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

# user BookMark Data
class SearchDataBookmarkAPIView(generics.CreateAPIView):
    queryset = SearchDataBookmark.objects.all()
    serializer_class = SearchDataBookmarkSerializer
    permission_classes = [IsAuthenticated]
    
class SearchDataBookmarkDeleteAPIView(generics.DestroyAPIView):
    queryset = SearchDataBookmark.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = SearchDataBookmarkDeleteSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.data)
        id = serializer.data.get("id")
        
        instance = SearchDataBookmark.objects.filter(id=id)
        
        if not instance:
            return Response({"error": "bookmark does not exist"})
        
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
  
    
    

class SearchDataShareAPIView(generics.CreateAPIView):
    queryset = SearchDataShare.objects.all()
    serializer_class = SearchDataShareSerializer
    

class SearchDataTotalListAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, *args, **kwargs):
        user = request.user
        profile = Profile.objects.get(user=user)
        total_searches = SearchDataHistory.objects.filter(user=profile).count()
        return Response({
            "user" : user.id,
            "total_searches" : total_searches
        })
        
        

# # Create (POST)
# class SearchDataUploadCreateView(generics.CreateAPIView):
#     queryset = SearchDataUpload.objects.all()
#     serializer_class = SearchDataUploadSerializer

# # Retrieve (GET single instance)
# class SearchDataUploadDetailView(generics.RetrieveAPIView):
#     queryset = SearchDataUpload.objects.filter(is_deleted=False)
#     serializer_class = SearchDataUploadSerializer

# # Update (PUT)
# class SearchDataUploadUpdateView(generics.UpdateAPIView):
#     queryset = SearchDataUpload.objects.filter(is_deleted=False)
#     serializer_class = SearchDataUploadSerializer

# # List (GET all non-deleted)
# class SearchDataUploadListView(generics.ListAPIView):
#     queryset = SearchDataUpload.objects.filter(is_deleted=False)
#     serializer_class = SearchDataUploadSerializer

# # Soft Delete (custom DELETE)
# class SearchDataUploadDeleteView(generics.DestroyAPIView):
#     queryset = SearchDataUpload.objects.filter(is_deleted=False)
#     serializer_class = SearchDataUploadSerializer

#     def delete(self, request, *args, **kwargs):
#         instance = self.get_object()
#         instance.is_deleted = True
#         instance.save()
#         return Response({"message": "Data successfully marked as deleted."}, status=status.HTTP_204_NO_CONTENT)
    
# Top 3 search keyword
class SearchDataTopSearchesView(generics.ListAPIView):
    serializer_class = TopSearchSerializer

    def get_queryset(self):
        return (
            SearchDataHistory.objects
            .values('search_query')
            .annotate(count=Count('search_query'))
            .order_by('-count')[:3]
        )
        
class SearchDataCountAPIView(APIView):
    def get(self, request, *args, **kwargs):
        saved_data = SearchDataSaved.objects.count()
        uploaded_data = SearchDataUpload.objects.count()
        shared_data =  SearchDataShare.objects.count()
        return Response({
            "saved_data" : saved_data,
            "uploaded_data" : uploaded_data,
            "shared_data" : shared_data,
            
        })