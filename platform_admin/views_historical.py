from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from accounts.models import Account, Profile
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib import messages

from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from accounts.forms import (RegistrationForm, AccountAuthenticationForm, 
                            AccountUpdateForm, UserProfileUpdateForm)
from accounts.models import Account, Profile
from django.conf import settings
from .forms import MarketSectorForm, MarketSectorBulkDataForm
from .models import MarketSectorBulkData, MarketSector, Historical
from .tasks import create_new_customers
from utility.models import Country, State, GeoPoliticalZone, City, Clan
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.views.generic import ( ListView, DetailView, CreateView, 
                                    UpdateView, DeleteView, RedirectView, View, TemplateView)



@login_required
def historical_detail_view(request, pk):
    object = MarketSector.objects.get(id=pk)
    context = {
        'object': object,
    }
    return render(request, 'platform_admin/historical/historical-detail.html', context)



@login_required
def historical_list_view(request):
    historicals = _load_historicals(request)
    # objects = MarketSector.objects.all().order_by('-date_created')
    context = {
        'historicals': historicals,
    }
    return render(request, 'platform_admin/historical/all-historicals.html', context)



@login_required
def list_load_historicals_view(request):
    historical = _load_historicals(request)
    context = {"historicals": historical,}
    return render(request, "platform_admin/historical/partials/all-historicals.html", context)



@login_required
def _load_historicals(request):
    page = request.GET.get("page")
    historicals = Historical.objects.all().order_by('-date_created')
    paginator = Paginator(historicals, 1)
    try:
        historicals = paginator.page(page)
    except PageNotAnInteger:
        historicals = paginator.page(1)
    except EmptyPage:
        historicals = paginator.page(paginator.num_pages)
    return historicals


@login_required
def historical_data_list_view(request):
    geo_politicals = GeoPoliticalZone.objects.all().order_by('name')
    states = State.objects.all().order_by('name')
    cities = City.objects.all().order_by('name')
    context = {
        'geo_politicals': geo_politicals,
        'states' : states,
        'cities' : cities,
    }
    return render(request, 'platform_admin/historical/historical-data-list-view.html', context)


###################################### BEGINNING OF GEOPOLITICAL ZONES FOR HISTORICAL DATA ###########################################

@login_required
def historical_geo_zone_detail_view(request, geozone_pk):
    object = GeoPoliticalZone.objects.get(id=geozone_pk)
    geozone_pk = geozone_pk
    objects = _load_historical_geo_zone_details(request, geozone_pk)
    context = {
        'object': object,
        'objects': objects,
        'states': State.objects.filter(geo_political_zone=object).order_by('name'),
    }
    return render(request, 'platform_admin/historical/historical-geo-zone-detail.html', context)



@login_required
def list_load_historical_geo_zone_details_view(request, geozone_pk):
    object = GeoPoliticalZone.objects.get(id=geozone_pk)
    historical_geo_zone_detail = _load_historical_geo_zone_details(request, geozone_pk)
    context = {"objects": historical_geo_zone_detail, 'object': object}
    return render(request, "platform_admin/historical/partials/historical_geo_zone_details.html", context)



@login_required
def _load_historical_geo_zone_details(request, geozone_pk):
    page = request.GET.get("page")
    historical_geo_zone_details = Historical.objects.filter(geo_political_zone=geozone_pk).order_by('-date_created')
    paginator = Paginator(historical_geo_zone_details, 1)
    try:
        historical_geo_zone_details = paginator.page(page)
    except PageNotAnInteger:
        historical_geo_zone_details = paginator.page(1)
    except EmptyPage:
        historical_geo_zone_details = paginator.page(paginator.num_pages)
    return historical_geo_zone_details

###################################### END OF GEOPOLITICAL ZONES FOR HISTORICAL DATA ###########################################



###################################### BEGINNING OF STATES LOCATION FOR HISTORICAL DATA ###########################################


@login_required
def historical_state_location_detail_view(request, state_location_pk):
    object = State.objects.get(id=state_location_pk)
    state_location_pk = state_location_pk
    objects = _load_historical_state_location_details(request, state_location_pk)
    context = {
        'object': object,
        'objects': objects,
        'cities': City.objects.filter(state=object).order_by('name'),
    }
    return render(request, 'platform_admin/historical/historical-state-location-detail.html', context)



@login_required
def list_load_historical_state_location_details_view(request, state_location_pk):
    object = State.objects.get(id=state_location_pk)
    historical_state_location_detail = _load_historical_state_location_details(request, state_location_pk)
    context = {"objects": historical_state_location_detail, 'object': object}
    return render(request, "platform_admin/historical/partials/historical_state_location_details.html", context)



@login_required
def _load_historical_state_location_details(request, state_location_pk):
    page = request.GET.get("page")
    historical_state_location_details = Historical.objects.filter(state=state_location_pk).order_by('-date_created')
    paginator = Paginator(historical_state_location_details, 1)
    try:
        historical_state_location_details = paginator.page(page)
    except PageNotAnInteger:
        historical_state_location_details = paginator.page(1)
    except EmptyPage:
        historical_state_location_details = paginator.page(paginator.num_pages)
    return historical_state_location_details

###################################### END OF STATES LOCATION FOR HISTORICAL DATA ###########################################




###################################### BEGINNING OF CITIES LOCATION FOR HISTORICAL DATA ###########################################


@login_required
def historical_city_location_detail_view(request, city_location_pk):
    object = City.objects.get(id=city_location_pk)
    city_location_pk = city_location_pk
    objects = _load_historical_city_location_details(request, city_location_pk)
    context = {
        'object': object,
        'objects': objects,
        'clans': Clan.objects.filter(city=object).order_by('name'),
    }
    return render(request, 'platform_admin/historical/historical-city-location-detail.html', context)



@login_required
def list_load_historical_city_location_details_view(request, city_location_pk):
    object = City.objects.get(id=city_location_pk)
    historical_city_location_detail = _load_historical_city_location_details(request, city_location_pk)
    context = {"objects": historical_city_location_detail, 'object': object}
    return render(request, "platform_admin/historical/partials/historical_city_location_details.html", context)



@login_required
def _load_historical_city_location_details(request, city_location_pk):
    page = request.GET.get("page")
    historical_city_location_details = Historical.objects.filter(city=city_location_pk).order_by('-date_created')
    paginator = Paginator(historical_city_location_details, 1)
    try:
        historical_city_location_details = paginator.page(page)
    except PageNotAnInteger:
        historical_city_location_details = paginator.page(1)
    except EmptyPage:
        historical_city_location_details = paginator.page(paginator.num_pages)
    return historical_city_location_details

###################################### END OF CITIES LOCATION FOR HISTORICAL DATA ###########################################




###################################### BEGINNING OF CLANS LOCATION FOR HISTORICAL DATA ###########################################


@login_required
def historical_clan_location_detail_view(request, clan_location_pk):
    object = Clan.objects.get(id=clan_location_pk)
    clan_location_pk = clan_location_pk
    objects = _load_historical_clan_location_details(request, clan_location_pk)
    context = {
        'object': object,
        'objects': objects,
    }
    return render(request, 'platform_admin/historical/historical-clan-location-detail.html', context)



@login_required
def list_load_historical_clan_location_details_view(request, clan_location_pk):
    object = Clan.objects.get(id=clan_location_pk)
    historical_clan_location_detail = _load_historical_clan_location_details(request, clan_location_pk)
    context = {"objects": historical_clan_location_detail, 'object': object}
    return render(request, "platform_admin/historical/partials/historical_clan_location_details.html", context)



@login_required
def _load_historical_clan_location_details(request, clan_location_pk):
    page = request.GET.get("page")
    historical_clan_location_details = Historical.objects.filter(clan=clan_location_pk).order_by('-date_created')
    paginator = Paginator(historical_clan_location_details, 1)
    try:
        historical_clan_location_details = paginator.page(page)
    except PageNotAnInteger:
        historical_clan_location_details = paginator.page(1)
    except EmptyPage:
        historical_clan_location_details = paginator.page(paginator.num_pages)
    return historical_clan_location_details

###################################### END OF CLANS LOCATION FOR HISTORICAL DATA ###########################################
