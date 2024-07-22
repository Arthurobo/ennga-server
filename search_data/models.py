from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from utility.utils import DATA_TYPE_CHOICES


class SearchDataCategory(models.Model):
    data_type = models.CharField(max_length=100, choices=DATA_TYPE_CHOICES, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)


class SearchDataSubCategory(models.Model):
    data_type = models.CharField(max_length=100, choices=DATA_TYPE_CHOICES, blank=True, null=True)
    category = models.ForeignKey("search_data.SearchDataCategory", blank=True, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=255, blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)


class SearchData(models.Model):
    data_id = models.IntegerField(blank=True, null=True)
    data_type = models.CharField(max_length=100, choices=DATA_TYPE_CHOICES, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    description = RichTextUploadingField(blank=True, null=True,)
    country = models.ForeignKey("utility.Country", blank=True, null=True, on_delete=models.SET_NULL)
    geo_political_zone = models.ForeignKey("utility.GeoPoliticalZone", blank=True, null=True, on_delete=models.SET_NULL)
    state = models.ForeignKey("utility.State", blank=True, null=True, on_delete=models.SET_NULL)
    city = models.ForeignKey("utility.City", blank=True, null=True, on_delete=models.SET_NULL)
    clan = models.ForeignKey("utility.Clan", blank=True, null=True, on_delete=models.SET_NULL)
    subclan = models.ForeignKey("utility.SubClan", blank=True, null=True, on_delete=models.SET_NULL)
    category = models.CharField(max_length=255, blank=True, null=True)
    sub_category = models.CharField(max_length=255, blank=True, null=True)
    data_category = models.ForeignKey("search_data.SearchDataCategory", blank=True, null=True, on_delete=models.SET_NULL)
    data_sub_category = models.ForeignKey("search_data.SearchDataSubCategory", blank=True, null=True, on_delete=models.SET_NULL)
    is_deleted = models.BooleanField(default=False)
    visualization_link = models.URLField(max_length=255, blank=True, null=True)
    other_references = models.JSONField(blank=True, null=True)
    visualization_link = models.URLField(max_length=255, blank=True, null=True)
    original_date_created = models.DateTimeField(blank=True, null=True)
    original_last_updated = models.DateTimeField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)
    

class SearchDataImages(models.Model):
    search_data = models.ForeignKey("search_data.SearchData", on_delete=models.CASCADE, blank=True, null=True)
    main_video = models.FileField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)
    

class SearchDataVideos(models.Model):
    search_data = models.ForeignKey("search_data.SearchData", on_delete=models.CASCADE, blank=True, null=True)
    main_video = models.FileField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)
    

class SearchDataMaps(models.Model):
    search_data = models.ForeignKey("search_data.SearchData", on_delete=models.CASCADE, blank=True, null=True)
    map_data = models.URLField(max_length=255, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)
    

class SearchDataNews(models.Model):
    search_data = models.ForeignKey("search_data.SearchData", on_delete=models.CASCADE, blank=True, null=True)
    news_data = models.URLField(max_length=255, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)
