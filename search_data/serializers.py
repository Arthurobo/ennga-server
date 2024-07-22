from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from .models import SearchData
from .documents import SearchDocument




class SearchDocumentSerializer(DocumentSerializer):
    class Meta(object):
        model = SearchData.objects.all()
        document = SearchDocument
        fields = ["id","data_id" ,"description"]
