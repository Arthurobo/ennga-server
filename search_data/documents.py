from django_elasticsearch_dsl import Document, Index, fields
from elasticsearch_dsl import analyzer, tokenizer
from .models import SearchData


INDEX = Index("search_data")

INDEX.settings(
    number_of_shards=1,
    number_of_replicas=1
)


autocomplete_analyzer = analyzer(
    'autocomplete_analyzer',
    tokenizer=tokenizer('trigram', 'ngram', min_gram=1, max_gram=20),
        filter=['lowercase']
    )


class SearchDocument(Document):
    id = fields.IntegerField(attr='id')
    data_type = fields.TextField(analyzer=autocomplete_analyzer)
    country = fields.ObjectField(
        properties={
            "id" : fields.IntegerField(attr="id"),
            "name" : fields.TextField(),
        }
    )
    geo_political_zone = fields.ObjectField(
        properties={
            "country" : fields.ObjectField(properties={
                "id" : fields.IntegerField(attr="id"),
                "name" : fields.TextField()
            }),
            "name" : fields.TextField(),

        }
    )
    state = fields.ObjectField(
        properties= {
            "id" :fields.IntegerField(attr='id'),
            "name" : fields.TextField(),
        }
    )
    city =  fields.ObjectField(
        properties= {
            "id" :fields.IntegerField(attr='id'),
            "name" : fields.TextField(),
        }
    ) 
    clan = fields.ObjectField(
        properties= {
            "id" :fields.IntegerField(attr='id'),
            "name" : fields.TextField(),
        }
    )
    subclan = fields.ObjectField(
        properties= {
            "id" :fields.IntegerField(attr='id'),
            "name" : fields.TextField(),
        }
    )
    category = fields.TextField()
    sub_category = fields.TextField()
    description = fields.TextField(fields={'raw': fields.KeywordField()})

    class Django:
        model = SearchData