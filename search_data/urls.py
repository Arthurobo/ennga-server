from django.urls import path
from .views import SearchDocumentView


app_name = "search_data"
urlpatterns = [
    path("search/", SearchDocumentView.as_view({'get': 'list'}))
]