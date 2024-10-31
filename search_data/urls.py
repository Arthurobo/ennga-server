from django.urls import path
from .views import SearchDocumentView,SearchTotalListAPIView


app_name = "search_data"
urlpatterns = [
    path("search/", SearchDocumentView.as_view({'get': 'list'})),
    path("search/total/<int:id>/", SearchTotalListAPIView.as_view()),
]