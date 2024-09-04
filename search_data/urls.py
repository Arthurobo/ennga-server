from django.urls import path
from .views import (
    SearchDocumentView,
    ImportDataListAPIView,
    ImportDataAPIView,
    RemoveDataAPIView
    )


app_name = "search_data"
urlpatterns = [
    path("search/", SearchDocumentView.as_view({'get': 'list'})),
    path("import-data/list/",ImportDataListAPIView.as_view() ),
    path("import-data/<int:pk>/",ImportDataAPIView.as_view()),
    path("remove-data/<int:pk>/",RemoveDataAPIView.as_view()),
    
]