from django.urls import path
from .views import (
    SearchDocumentView,
    SearchTotalListAPIView,
    SearchDataImportListAPIView,
    SearchDataImportAPIView,
    SearchDataBookmarkListAPIView,
    SearchDataBookmarkAPIView,
    )


app_name = "search_data"
urlpatterns = [
    path("search/", SearchDocumentView.as_view({'get': 'list'})),
    path("search/total/<int:id>/", SearchTotalListAPIView.as_view()),
    path("search/import/list/",SearchDataImportListAPIView.as_view() ),
    path("search/import/",SearchDataImportAPIView.as_view()),

    path("search/bookmark/list/",SearchDataBookmarkListAPIView.as_view() ),
    path("search/bookmark/",SearchDataBookmarkAPIView.as_view()),
]