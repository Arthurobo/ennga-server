from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from .models import (SearchData, 
                     SearchDataImport,
                     SearchDataBookmark,
                     SearchDataShare,
)
from .documents import SearchDocument
from rest_framework import serializers
from .models import SearchDataUpload



class SearchDocumentSerializer(DocumentSerializer):
    class Meta(object):
        model = SearchData.objects.all()
        document = SearchDocument
        fields = ["id", "title", "description"]



class SearchDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchData
        fields = ["id", "title", "description"]

class SearchDataImportListSerializer(serializers.ModelSerializer):
    search_data = SearchDataSerializer()
    class Meta:
        model = SearchDataImport
        fields = ["id", "search_data"]


class SearchDataImportSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchDataImport
        fields = ["user", "search_data"]



class SearchDataBookmarkListSerializer(serializers.ModelSerializer):
    search_data = SearchDataSerializer()
    class Meta:
        model = SearchDataBookmark
        fields = ["id", "search_data"]


class SearchDataBookmarkDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchDataBookmark
        fields = ["id"]
        
        
class SearchDataBookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchDataBookmark
        fields = ["user", "search_data"]



class SearchDataCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchData
        fields = ["data_id", "data_type", "title", "description", "country", 
                  "geo_political_zone","state","city","clan", "subclan", 
                  "category", "sub_category", "data_category", "data_sub_category", "other_references", "visualization_link"]



class SearchDataUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchData
        fields = ["data_id", "data_type", "title", "description", "country", 
                  "geo_political_zone","state","city","clan", "subclan", 
                  "category", "sub_category", "data_category", "data_sub_category", "other_references", "visualization_link"]



class SearchDataDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchData
        fields = ["is_deleted"]
        
        
class SearchDataShareSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchDataShare
        fields = ["user", "search_data", "platform"]
        
        

class SearchDataUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchDataUpload
        fields = ['id', 'user', 'file', 'is_deleted', 'date_created', 'last_updated']
        read_only_fields = ['date_created', 'last_updated']


class TopSearchSerializer(serializers.Serializer):
    search_query = serializers.CharField()
    count = serializers.IntegerField()