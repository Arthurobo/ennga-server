from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from .models import SearchData
from .documents import SearchDocument
from rest_framework import serializers


class SearchDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchData
        fields = ["id","data_id", "title", "description"]


class SearchDocumentSerializer(DocumentSerializer):
    class Meta(object):
        model = SearchData.objects.all()
        document = SearchDocument
        fields = ["id","data_id", "title", "description"]
