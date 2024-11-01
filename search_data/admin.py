from django.contrib import admin
from .models import SearchData, SearchDataImport, SearchDataBookmark
# Register your models here.

admin.site.register(SearchData)

admin.site.register(SearchDataImport)
admin.site.register(SearchDataBookmark)