from django.db import models
from django.urls import reverse


class Country(models.Model):
    name = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Countries'
    

class Tribe(models.Model):
    name = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Tribes"

    class Meta:
        ordering = ['name',]


class GeoPoliticalZone(models.Model):
    country = models.ForeignKey(Country, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=255)
    managers = models.ManyToManyField("accounts.Profile", blank=True, related_name='geo_political_zone_managers')
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
        
    class Meta:
        verbose_name_plural = 'Geo Political Zones'

    class Meta:
        ordering = ['name',]


    def get_historical_geo_zone_detail_url(self):
        return reverse('platform_admin:historical-geo-zone-detail-view', kwargs={'geozone_pk': self.pk})

    def get_list_load_historical_geo_zone_details_url(self):
        return reverse('platform_admin:list-load-historical-geo-zone-details-view', kwargs={'geozone_pk': self.pk})


    def get_market_sector_geo_zone_detail_url(self):
        return reverse('platform_admin:market-sector-geo-zone-detail-view', kwargs={'geozone_pk': self.pk})

    def get_list_load_market_sector_geo_zone_details_url(self):
        return reverse('platform_admin:list-load-market-sector-geo-zone-details-view', kwargs={'geozone_pk': self.pk})


    def get_geo_physical_geo_zone_detail_url(self):
        return reverse('platform_admin:geo-physical-geo-zone-detail-view', kwargs={'geozone_pk': self.pk})

    def get_list_load_geo_physical_geo_zone_details_url(self):
        return reverse('platform_admin:list-load-geo-physical-geo-zone-details-view', kwargs={'geozone_pk': self.pk})

    def get_market_sector_geo_political_zone_create_view_url(self):
        return reverse('platform_admin:market-sector-geo-political-zone-create-view', kwargs={'geozone_pk': self.pk})

    def get_historical_geo_political_zone_create_view_url(self):
        return reverse('platform_admin:historical-geo-political-zone-create-view', kwargs={'geozone_pk': self.pk})

    def get_geo_physical_geo_political_zone_create_view_url(self):
        return reverse('platform_admin:geo-physical-geo-political-zone-create-view', kwargs={'geozone_pk': self.pk})


class State(models.Model):
    country = models.ForeignKey(Country, null=True, on_delete=models.SET_NULL)
    geo_political_zone = models.ForeignKey(GeoPoliticalZone, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=255)
    managers = models.ManyToManyField("accounts.Profile", blank=True, related_name='state_managers')
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
        
    class Meta:
        verbose_name_plural = 'States'

    class Meta:
        ordering = ['name',]


    def get_historical_state_location_detail_url(self):
        return reverse('platform_admin:historical-state-location-detail-view', kwargs={'state_location_pk': self.pk})

    def get_list_load_historical_state_location_details_url(self):
        return reverse('platform_admin:list-load-historical-state-location-details-view', kwargs={'state_location_pk': self.pk})


    def get_market_sector_state_location_detail_url(self):
        return reverse('platform_admin:market-sector-state-location-detail-view', kwargs={'state_location_pk': self.pk})

    def get_list_load_market_sector_state_location_details_url(self):
        return reverse('platform_admin:list-load-market-sector-state-location-details-view', kwargs={'state_location_pk': self.pk})


    def get_geo_physical_state_location_detail_url(self):
        return reverse('platform_admin:geo-physical-state-location-detail-view', kwargs={'state_location_pk': self.pk})

    def get_list_load_geo_physical_state_location_details_url(self):
        return reverse('platform_admin:list-load-geo-physical-state-location-details-view', kwargs={'state_location_pk': self.pk})

    def get_market_sector_state_create_view_url(self):
        return reverse('platform_admin:market-sector-state-create-view', kwargs={'state_location_pk': self.pk})

    def get_historical_state_create_view_url(self):
        return reverse('platform_admin:historical-state-create-view', kwargs={'state_location_pk': self.pk})

    def get_geo_physical_state_create_view_url(self):
        return reverse('platform_admin:geo-physical-state-create-view', kwargs={'state_location_pk': self.pk})


class City(models.Model):
    country = models.ForeignKey(Country, null=True, on_delete=models.SET_NULL)
    geo_political_zone = models.ForeignKey(GeoPoliticalZone, null=True, on_delete=models.SET_NULL)
    state = models.ForeignKey(State, null=True, on_delete=models.SET_NULL)
    tribe = models.ForeignKey(Tribe, blank=True, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=255)
    managers = models.ManyToManyField("accounts.Profile", blank=True, related_name='city_managers')
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Cities"
        ordering = ['name',]


    def get_historical_city_location_detail_url(self):
        return reverse('platform_admin:historical-city-location-detail-view', kwargs={'city_location_pk': self.pk})

    def get_list_load_historical_city_location_details_url(self):
        return reverse('platform_admin:list-load-historical-city-location-details-view', kwargs={'city_location_pk': self.pk})


    def get_market_sector_city_location_detail_url(self):
        return reverse('platform_admin:market-sector-city-location-detail-view', kwargs={'city_location_pk': self.pk})

    def get_list_load_market_sector_city_location_details_url(self):
        return reverse('platform_admin:list-load-market-sector-city-location-details-view', kwargs={'city_location_pk': self.pk})


    def get_geo_physical_city_location_detail_url(self):
        return reverse('platform_admin:geo-physical-city-location-detail-view', kwargs={'city_location_pk': self.pk})

    def get_list_load_geo_physical_city_location_details_url(self):
        return reverse('platform_admin:list-load-geo-physical-city-location-details-view', kwargs={'city_location_pk': self.pk})

    def get_market_sector_city_create_view_url(self):
        return reverse('platform_admin:market-sector-city-create-view', kwargs={'city_location_pk': self.pk})

    def get_historical_city_create_view_url(self):
        return reverse('platform_admin:historical-city-create-view', kwargs={'city_location_pk': self.pk})

    def get_geo_physical_city_create_view_url(self):
        return reverse('platform_admin:geo-physical-city-create-view', kwargs={'city_location_pk': self.pk})
    

class Clan(models.Model):
    country = models.ForeignKey(Country, null=True, on_delete=models.SET_NULL)
    geo_political_zone = models.ForeignKey(GeoPoliticalZone, null=True, on_delete=models.SET_NULL)
    state = models.ForeignKey(State, null=True, on_delete=models.SET_NULL)
    city = models.ForeignKey(City, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=255)
    managers = models.ManyToManyField("accounts.Profile", blank=True, related_name='clan_managers')
    restricted_users = models.ManyToManyField("accounts.Profile", blank=True, related_name='clan_restricted_users')
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Clans"

    class Meta:
        ordering = ['name',]


    def get_historical_clan_location_detail_url(self):
        return reverse('platform_admin:historical-clan-location-detail-view', kwargs={'clan_location_pk': self.pk})

    def get_list_load_historical_clan_location_details_url(self):
        return reverse('platform_admin:list-load-historical-clan-location-details-view', kwargs={'clan_location_pk': self.pk})

    def get_market_sector_clan_location_detail_url(self):
        return reverse('platform_admin:market-sector-clan-location-detail-view', kwargs={'clan_location_pk': self.pk})

    def get_list_load_market_sector_clan_location_details_url(self):
        return reverse('platform_admin:list-load-market-sector-clan-location-details-view', kwargs={'clan_location_pk': self.pk})

    def get_geo_physical_clan_location_detail_url(self):
        return reverse('platform_admin:geo-physical-clan-location-detail-view', kwargs={'clan_location_pk': self.pk})

    def get_list_load_geo_physical_clan_location_details_url(self):
        return reverse('platform_admin:list-load-geo-physical-clan-location-details-view', kwargs={'clan_location_pk': self.pk})

    def get_market_sector_clan_create_view_url(self):
        return reverse('platform_admin:market-sector-clan-create-view', kwargs={'clan_location_pk': self.pk})

    def get_historical_clan_create_view_url(self):
        return reverse('platform_admin:historical-clan-create-view', kwargs={'clan_location_pk': self.pk})

    def get_geo_physical_clan_create_view_url(self):
        return reverse('platform_admin:geo-physical-clan-create-view', kwargs={'clan_location_pk': self.pk})
    

class SubClan(models.Model):
    country = models.ForeignKey(Country, null=True, on_delete=models.SET_NULL)
    geo_political_zone = models.ForeignKey(GeoPoliticalZone, null=True, on_delete=models.SET_NULL)
    state = models.ForeignKey(State, null=True, on_delete=models.SET_NULL)
    city = models.ForeignKey(City, null=True, on_delete=models.SET_NULL)
    clan = models.ForeignKey(Clan, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=255)
    managers = models.ManyToManyField("accounts.Profile", blank=True, related_name='subclan_managers')
    restricted_users = models.ManyToManyField("accounts.Profile", blank=True, related_name='subclan_restricted_users')
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Clans"

    class Meta:
        ordering = ['name',]
