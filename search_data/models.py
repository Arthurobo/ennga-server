from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from utility.utils import DATA_TYPE_CHOICES


class SearchData(models.Model):
    data_id = models.IntegerField(blank=True, null=True)
    data_type = models.CharField(max_length=100, choices=DATA_TYPE_CHOICES, blank=True, null=True)
    country = models.ForeignKey("utility.Country", blank=True, null=True, on_delete=models.SET_NULL)
    geo_political_zone = models.ForeignKey("utility.GeoPoliticalZone", null=True, on_delete=models.SET_NULL)
    state = models.ForeignKey("utility.State", blank=True, null=True, on_delete=models.SET_NULL)
    city = models.ForeignKey("utility.City", blank=True, null=True, on_delete=models.SET_NULL)
    clan = models.ForeignKey("utility.Clan", blank=True, null=True, on_delete=models.SET_NULL)
    subclan = models.ForeignKey("utility.SubClan", blank=True, null=True, on_delete=models.SET_NULL)
    category = models.CharField(max_length=255, blank=True, null=True)
    sub_category = models.CharField(max_length=255, blank=True, null=True)
    description = RichTextUploadingField(blank=True, null=True,)
    is_deleted = models.BooleanField(default=False)
    original_date_created = models.DateTimeField(blank=True, null=True)
    original_last_updated = models.DateTimeField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)