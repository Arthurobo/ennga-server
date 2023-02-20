# from django.urls import path
# from django.contrib.auth import views as auth_views
# from django.views.generic import TemplateView

# from .views import dashboard, edit_account_view, UpdatePassword, ProfileDetailView, profile_market_sector_view, profile_load_market_sectors_view, all_users, approved_users, admin_users
# from .views_market_sector import market_sector_list_view, market_sector_create_view, list_load_market_sectors_view, market_sector_upload_view

# from .views_geo_political import geo_political_list_view, geo_political_create_view, list_load_geo_politicals_view, geo_political_upload_view

# from .views_historical import historical_data_list_view, historical_geo_zone_detail_view

# app_name = "platform_admin"

# urlpatterns = [
#     path('', dashboard, name='dashboard'),
#     path('all-users/', all_users, name='all-users'),
#     path('approved-users/', approved_users, name='approved-users'),
#     path('admin-users/', admin_users, name='admin-users'),

#     path('<user_id>/edit/', edit_account_view, name='edit-account'),
#     path('change-password/', UpdatePassword.as_view(), name="update_password"),
    
#     path('<int:pk>/', ProfileDetailView.as_view(), name='user-profile-view'),
#     path('<int:pk>/market-sector/', profile_market_sector_view, name='user-market-sector-view'),
#     path('<int:pk>/market-sector/load/', profile_load_market_sectors_view, name='profile_market_sectors'),


#     # Beginning of market sector
#     path('market-sector/create/', market_sector_create_view, name="market-sector-create-view"),
#     path('market-sector/upload/', market_sector_upload_view, name="market-sector-upload-view"),


#     path('market-sector/', market_sector_list_view, name="market-sector-list-view"),
#     path('market-sector/load/', list_load_market_sectors_view, name='market_sectors'),


#     path('geo-political/', geo_political_list_view, name="geo-political-list-view"),
#     path('geo-political/load/', list_load_geo_politicals_view, name='geo_politicals'),


#     path('historical-data-list/', historical_data_list_view, name='historical-data-list-view'),
#     path('historical-geo-zone-detail-view/<int:pk>/', historical_geo_zone_detail_view, name='historical-geo-zone-detail-view'),

                                                                 
# ]

































































from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

from .views import dashboard, edit_account_view, UpdatePassword, ProfileDetailView, profile_market_sector_view, profile_load_market_sectors_view, all_users, approved_users, admin_users
from .views_market_sector import (
    market_sector_data_list_view, market_sector_geo_zone_detail_view, list_load_market_sector_geo_zone_details_view, 
    market_sector_state_location_detail_view, list_load_market_sector_state_location_details_view, 
    market_sector_city_location_detail_view,
    list_load_market_sector_city_location_details_view, market_sector_clan_location_detail_view, list_load_market_sector_clan_location_details_view,
    market_sector_detail_view, user_market_sector_list_view, list_load_user_market_sectors_view
)


from .views_historical import (historical_list_view,
    list_load_historicals_view,
    historical_data_list_view, historical_geo_zone_detail_view, list_load_historical_geo_zone_details_view, 
    historical_state_location_detail_view, list_load_historical_state_location_details_view, 
    historical_city_location_detail_view,
    list_load_historical_city_location_details_view, historical_clan_location_detail_view, list_load_historical_clan_location_details_view,
    historical_detail_view, historical_create_view, user_historical_list_view, list_load_user_historicals_view
)

from .views_geo_physical import (
    geo_physical_detail_view, geo_physical_list_view, list_load_geo_physicals_view, geo_physical_create_view, geo_physical_data_list_view,
    user_geo_physical_list_view, list_load_user_geo_physicals_view, geo_physical_geo_zone_detail_view,
list_load_geo_physical_geo_zone_details_view, geo_physical_state_location_detail_view, list_load_geo_physical_state_location_details_view,
geo_physical_city_location_detail_view, list_load_geo_physical_city_location_details_view,
geo_physical_clan_location_detail_view, list_load_geo_physical_clan_location_details_view
)

from .views import dashboard, edit_account_view, UpdatePassword, ProfileDetailView, profile_market_sector_view, profile_load_market_sectors_view, all_users, approved_users, admin_users
from .views_market_sector import (market_sector_list_view, market_sector_create_view, list_load_market_sectors_view, market_sector_upload_view,
)


app_name = "platform_admin"

urlpatterns = [
    path('home/', dashboard, name='dashboard'),
    path('all-users/', all_users, name='all-users'),
    path('approved-users/', approved_users, name='approved-users'),
    path('admin-users/', admin_users, name='admin-users'),

    path('<user_id>/edit/', edit_account_view, name='edit-account'),
    path('change-password/', UpdatePassword.as_view(), name="update_password"),
    
    path('<int:pk>/', ProfileDetailView.as_view(), name='user-profile-view'),
    path('<int:pk>/market-sector/', profile_market_sector_view, name='user-market-sector-view'),
    path('<int:pk>/market-sector/load/', profile_load_market_sectors_view, name='profile_market_sectors'),





    #""" Beginning of hISTORIC DATA """
    path('historical/create/', historical_create_view, name="historical-create-view"),
    path('historical/', historical_list_view, name="historical-list-view"), # Lists all the data in market sectors
    path('historical/load/', list_load_historicals_view, name='historicals'),
    path('historical-data-list/', historical_data_list_view, name='historical-data-list-view'),
    path('historical-detail/<int:pk>/', historical_detail_view, name='historical-detail-view'),


    ###################################### BEGINNING OF LOGGED IN USER HISTORICAL DATA ###########################################
    path('historical/user/', user_historical_list_view, name="user-historical-list-view"), # Lists all the data in market sectors
    path('historical/load/user/', list_load_user_historicals_view, name='user_historicals'),
    ###################################### END OF LOGGED IN USER HISTORICAL DATA ###########################################


    ###################################### BEGINNING OF GEOPOLITICAL ZONES FOR HISTORICAL DATA ###########################################
    path('historical-geo-zone-detail-view/<int:geozone_pk>/', historical_geo_zone_detail_view, name='historical-geo-zone-detail-view'),
    path('historical-geo-zone-detail-view/<int:geozone_pk>/load/', list_load_historical_geo_zone_details_view, name='list-load-historical-geo-zone-details-view'),

    ###################################### END OF GEOPOLITICAL ZONES FOR HISTORICAL DATA ###########################################
    

    ###################################### BEGINNING OF STATES LOCATION FOR HISTORICAL DATA ###########################################

    path('historical-state-location-detail-view/<int:state_location_pk>/', historical_state_location_detail_view, name='historical-state-location-detail-view'),
    path('historical-state-location-detail-view/<int:state_location_pk>/load/', list_load_historical_state_location_details_view, name='list-load-historical-state-location-details-view'),

    ###################################### END OF STATES LOCATION FOR HISTORICAL DATA ###########################################
    

    ###################################### BEGINNING OF CITIES LOCATION FOR HISTORICAL DATA ###########################################

    path('historical-city-location-detail-view/<int:city_location_pk>/', historical_city_location_detail_view, name='historical-city-location-detail-view'),
    path('historical-city-location-detail-view/<int:city_location_pk>/load/', list_load_historical_city_location_details_view, name='list-load-historical-city-location-details-view'),

    ###################################### END OF CITIES LOCATION FOR HISTORICAL DATA ###########################################
    

    ###################################### BEGINNING OF CLANS LOCATION FOR HISTORICAL DATA ###########################################

    path('historical-clan-location-detail-view/<int:clan_location_pk>/', historical_clan_location_detail_view, name='historical-clan-location-detail-view'),
    path('historical-clan-location-detail-view/<int:clan_location_pk>/load/', list_load_historical_clan_location_details_view, name='list-load-historical-clan-location-details-view'),

    ###################################### END OF CLANS LOCATION FOR HISTORICAL DATA ###########################################


    #""" Beginning of MARKET SECTOR DATA 
    path('market-sector/create/', market_sector_create_view, name="market-sector-create-view"),
    path('market-sector/upload/', market_sector_upload_view, name="market-sector-upload-view"),
    path('market-sector/', market_sector_list_view, name="market-sector-list-view"), # Lists all the data in market sectors
    path('market-sector/load/', list_load_market_sectors_view, name='market_sectors'),
    path('market-sector-data-list/', market_sector_data_list_view, name='market-sector-data-list-view'),
    path('market-sector-detail/<int:pk>/', market_sector_detail_view, name='market-sector-detail-view'),

    ###################################### BEGINNING OF LOGGED IN USER MARKET_SECTOR DATA ###########################################
    path('market-sector/user/', user_market_sector_list_view, name="user-market-sector-list-view"), # Lists all the data in market sectors
    path('market-sector/load/user/', list_load_user_market_sectors_view, name='user_market_sectors'),
    ###################################### END OF LOGGED IN USER MARKET_SECTOR DATA ###########################################

    ###################################### BEGINNING OF GEOPOLITICAL ZONES FOR MARKET_SECTOR DATA ###########################################
    path('market-sector-geo-zone-detail-view/<int:geozone_pk>/', market_sector_geo_zone_detail_view, name='market-sector-geo-zone-detail-view'),
    path('market-sector-geo-zone-detail-view/<int:geozone_pk>/load/', list_load_market_sector_geo_zone_details_view, name='list-load-market-sector-geo-zone-details-view'),

    ###################################### END OF GEOPOLITICAL ZONES FOR HISTORICAL DATA ###########################################
    

    ###################################### BEGINNING OF STATES LOCATION FOR HISTORICAL DATA ###########################################

    path('market-sector-state-location-detail-view/<int:state_location_pk>/', market_sector_state_location_detail_view, name='market-sector-state-location-detail-view'),
    path('market-sector-state-location-detail-view/<int:state_location_pk>/load/', list_load_market_sector_state_location_details_view, name='list-load-market-sector-state-location-details-view'),

    ###################################### END OF STATES LOCATION FOR HISTORICAL DATA ###########################################
    

    ###################################### BEGINNING OF CITIES LOCATION FOR HISTORICAL DATA ###########################################

    path('market-sector-city-location-detail-view/<int:city_location_pk>/', market_sector_city_location_detail_view, name='market-sector-city-location-detail-view'),
    path('market-sector-city-location-detail-view/<int:city_location_pk>/load/', list_load_market_sector_city_location_details_view, name='list-load-market-sector-city-location-details-view'),

    ###################################### END OF CITIES LOCATION FOR HISTORICAL DATA ###########################################
    

    ###################################### BEGINNING OF CLANS LOCATION FOR HISTORICAL DATA ###########################################

    path('market-sector-clan-location-detail-view/<int:clan_location_pk>/', market_sector_clan_location_detail_view, name='market-sector-clan-location-detail-view'),
    path('market-sector-clan-location-detail-view/<int:clan_location_pk>/load/', list_load_market_sector_clan_location_details_view, name='list-load-market-sector-clan-location-details-view'),

    ###################################### END OF CLANS LOCATION FOR HISTORICAL DATA ###########################################





















    #""" Beginning of MARKET SECTOR DATA 
    path('geo-physical/create/', geo_physical_create_view, name="geo-physical-create-view"),
    # path('market-sector/upload/', market_sector_upload_view, name="market-sector-upload-view"),
    path('geo-physical/', geo_physical_list_view, name="geo-physical-list-view"), # Lists all the data in market sectors
    path('geo-physical/load/', list_load_geo_physicals_view, name='geo_physicals'),
    path('geo-physical-data-list/', geo_physical_data_list_view, name='geo-physical-data-list-view'),
    path('geo-physical-detail/<int:pk>/', geo_physical_detail_view, name='geo-physical-detail-view'),

    # ###################################### BEGINNING OF LOGGED IN USER GEO_PHYSICAL DATA ###########################################
    path('geo-physical/user/', user_geo_physical_list_view, name="user-geo-physical-list-view"), # Lists all the data in market sectors
    path('geo-physical/load/user/', list_load_user_geo_physicals_view, name='user_geo_physicals'),
    # ###################################### END OF LOGGED IN USER GEO_PHYSICAL DATA ###########################################

    # ###################################### BEGINNING OF GEOPOLITICAL ZONES FOR GEO_PHYSICAL DATA ###########################################
    path('geo-physical-geo-zone-detail-view/<int:geozone_pk>/', geo_physical_geo_zone_detail_view, name='geo-physical-geo-zone-detail-view'),
    path('geo-physical-geo-zone-detail-view/<int:geozone_pk>/load/', list_load_geo_physical_geo_zone_details_view, name='list-load-geo-physical-geo-zone-details-view'),

    # ###################################### END OF GEOPOLITICAL ZONES FOR GEO_PHYSICAL DATA ###########################################
    

    # ###################################### BEGINNING OF STATES LOCATION FOR GEO_PHYSICAL DATA ###########################################

    path('geo-physical-state-location-detail-view/<int:state_location_pk>/', geo_physical_state_location_detail_view, name='geo-physical-state-location-detail-view'),
    path('geo-physical-state-location-detail-view/<int:state_location_pk>/load/', list_load_geo_physical_state_location_details_view, name='list-load-geo-physical-state-location-details-view'),

    # ###################################### END OF STATES LOCATION FOR GEO_PHYSICAL DATA ###########################################
    

    # ###################################### BEGINNING OF CITIES LOCATION FOR GEO_PHYSICAL DATA ###########################################

    path('geo-physical-city-location-detail-view/<int:city_location_pk>/', geo_physical_city_location_detail_view, name='geo-physical-city-location-detail-view'),
    path('geo-physical-city-location-detail-view/<int:city_location_pk>/load/', list_load_geo_physical_city_location_details_view, name='list-load-geo-physical-city-location-details-view'),

    # ###################################### END OF CITIES LOCATION FOR GEO_PHYSICAL DATA ###########################################
    

    # ###################################### BEGINNING OF CLANS LOCATION FOR GEO_PHYSICAL DATA ###########################################

    path('geo-physical-clan-location-detail-view/<int:clan_location_pk>/', geo_physical_clan_location_detail_view, name='geo-physical-clan-location-detail-view'),
    path('geo-physical-clan-location-detail-view/<int:clan_location_pk>/load/', list_load_geo_physical_clan_location_details_view, name='list-load-geo-physical-clan-location-details-view'),

    # ###################################### END OF CLANS LOCATION FOR GEO_PHYSICAL DATA ###########################################
                                                                 
]
