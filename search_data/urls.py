from django.urls import path
from .views_search import SearchDocumentView


app_name = "search_data"
urlpatterns = [
    path("search/", SearchDocumentView.as_view({'get': 'list'}))
]