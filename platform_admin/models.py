from django.db import models
from accounts.models import Profile
from utility.models import Country, State, City, GeoPoliticalZone


class MarketSectorCategory(models.Model):
    name = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Market Sector Categories'


class MarketSectorBulkData(models.Model):
    user = models.ForeignKey("accounts.Profile", blank=True, null=True, on_delete=models.SET_NULL)
    country = models.ForeignKey("utility.Country", blank=True, null=True, on_delete=models.SET_NULL)
    state = models.ForeignKey("utility.State", blank=True, null=True, on_delete=models.SET_NULL)
    city = models.ForeignKey("utility.City", blank=True, null=True, on_delete=models.SET_NULL)
    category = models.ForeignKey(MarketSectorCategory, null=True, on_delete=models.SET_NULL)
    filez = models.FileField(upload_to='customers/csv')
    activated = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"File id: {self.id}"
    

class MarketSector(models.Model):
    user = models.ForeignKey("accounts.Profile", blank=True, null=True, on_delete=models.SET_NULL)
    bulk_data = models.ForeignKey('MarketSectorBulkData', blank=True, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=255)
    category = models.ForeignKey(MarketSectorCategory, null=True, on_delete=models.SET_NULL)
    country = models.ForeignKey("utility.Country", blank=True, null=True, on_delete=models.SET_NULL)
    geo_political_zone = models.ForeignKey(GeoPoliticalZone, null=True, on_delete=models.SET_NULL)
    state = models.ForeignKey("utility.State", blank=True, null=True, on_delete=models.SET_NULL)
    city = models.ForeignKey("utility.City", blank=True, null=True, on_delete=models.SET_NULL)
    clan = models.ForeignKey("utility.Clan", blank=True, null=True, on_delete=models.SET_NULL)
    address_location = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    

class HistoricalCategory(models.Model):
    name = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Historical Categories'


class Historical(models.Model):
    user = models.ForeignKey("accounts.Profile", blank=True, null=True, on_delete=models.SET_NULL)
    country = models.ForeignKey("utility.Country", blank=True, null=True, on_delete=models.SET_NULL)
    geo_political_zone = models.ForeignKey(GeoPoliticalZone, null=True, on_delete=models.SET_NULL)
    state = models.ForeignKey("utility.State", blank=True, null=True, on_delete=models.SET_NULL)
    city = models.ForeignKey("utility.City", blank=True, null=True, on_delete=models.SET_NULL)
    clan = models.ForeignKey("utility.Clan", blank=True, null=True, on_delete=models.SET_NULL)
    category = models.ForeignKey(HistoricalCategory, null=True, on_delete=models.SET_NULL)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)


class GeoPoliticalCategory(models.Model):
    name = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Geo Political Categories'


class GeoPoliticalData(models.Model):
    user = models.ForeignKey("accounts.Profile", blank=True, null=True, on_delete=models.SET_NULL)
    country = models.ForeignKey("utility.Country", blank=True, null=True, on_delete=models.SET_NULL)
    geo_political_zone = models.ForeignKey(GeoPoliticalZone, null=True, on_delete=models.SET_NULL)
    state = models.ForeignKey("utility.State", blank=True, null=True, on_delete=models.SET_NULL)
    city = models.ForeignKey("utility.City", blank=True, null=True, on_delete=models.SET_NULL)
    clan = models.ForeignKey("utility.Clan", blank=True, null=True, on_delete=models.SET_NULL)
    category = models.ForeignKey(GeoPoliticalCategory, null=True, on_delete=models.SET_NULL)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)