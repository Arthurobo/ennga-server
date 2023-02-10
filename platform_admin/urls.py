from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

from .views import dashboard, edit_account_view, UpdatePassword, ProfileDetailView, profile_market_sector_view, profile_load_market_sectors_view
from .views_market_sector import market_sector_list_view, market_sector_create_view, list_load_market_sectors_view, market_sector_upload_view

app_name = "platform_admin"

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('<user_id>/edit/', edit_account_view, name='edit-account'),
    path('change-password/', UpdatePassword.as_view(), name="update_password"),
    
    path('<int:pk>/', ProfileDetailView.as_view(), name='user-profile-view'),
    path('<int:pk>/market-sector/', profile_market_sector_view, name='user-market-sector-view'),
    path('<int:pk>/market-sector/load/', profile_load_market_sectors_view, name='profile_market_sectors'),


    # Beginning of market sector
    path('market-sector/create/', market_sector_create_view, name="market-sector-create-view"),
    path('market-sector/upload/', market_sector_upload_view, name="market-sector-upload-view"),


    path('market-sector/', market_sector_list_view, name="market-sector-list-view"),
    path('market-sector/load/', list_load_market_sectors_view, name='market_sectors'),

                                                                 
]
