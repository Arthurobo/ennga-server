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
from .forms import HistoricalForm, HistoricalGeoPoliticalZoneForm, HistoricalStateForm, HistoricalCityForm, HistoricalClanForm
from .models import MarketSectorBulkData, MarketSector, Historical, HistoricalCategory
from .tasks import create_new_customers
from utility.models import Country, State, GeoPoliticalZone, City, Clan
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.views.generic import ( ListView, DetailView, CreateView, 
                                    UpdateView, DeleteView, RedirectView, View, TemplateView)
from .forms import Historical


@login_required
def historical_detail_view(request, pk):
    object = Historical.objects.get(id=pk)
    form = HistoricalForm(request.POST or None, request.FILES or None, instance=object)

    if request.htmx:
        template_name = 'platform_admin/historical/partials/ajax_historical_update.html'

    if form.is_valid():
        # form.instance.user = request.user.account_profile
        form.save()
        messages.success(request, "Data added successfully!!!")
        return HttpResponseRedirect(reverse('platform_admin:historical-detail-view', kwargs={'pk': pk} ))
    
    context = {
        'object': object,
        'form': form,
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
    paginator = Paginator(historicals, 20)
    try:
        historicals = paginator.page(page)
    except PageNotAnInteger:
        historicals = paginator.page(1)
    except EmptyPage:
        historicals = paginator.page(paginator.num_pages)
    return historicals






################## BEGINNING OF VARIOUS LOCATION DATA ENTRY CENTERS ###########################################
@login_required
def historical_create_view(request):
    form = HistoricalForm(request.POST or None, request.FILES or None)

    if request.htmx:
        template_name = 'platform_admin/historical/partials/ajax_historical_create.html'

    if form.is_valid():
        nigeria_as_country_location = Country.objects.get(id=1)

        form.instance.user = request.user.account_profile
        form.instance.country = nigeria_as_country_location
        newly_saved_form = form.save()
        # messages.success(request, "Data added successfully!!!")
        # return HttpResponseRedirect(reverse('platform_admin:market-sector-create-view'))

    context = {
    'form': form,
    }
    return render(request, 'platform_admin/historical/historical-create.html', context)


@login_required
def historical_geo_political_zone_create_view(request, geozone_pk):
    geo_political_zone = GeoPoliticalZone.objects.get(id=geozone_pk)
    form = HistoricalGeoPoliticalZoneForm(request.POST or None, request.FILES or None, geozone_pk=geozone_pk)

    if request.htmx:
        template_name = 'platform_admin/historical/partials/historical-geo-political-zone-create.html'

    if form.is_valid():
        nigeria_as_country_location = Country.objects.get(id=1)

        form.instance.user = request.user.account_profile
        form.instance.country = nigeria_as_country_location
        form.instance.geo_political_zone = geo_political_zone
        newly_saved_form = form.save()
        # messages.success(request, "Data added successfully!!!")
        # return HttpResponseRedirect(reverse('platform_admin:market-sector-create-view'))

    context = {
    'form': form,
    'object': geo_political_zone,
    }
    return render(request, 'platform_admin/historical/historical-geo-political-zone-create.html', context)


@login_required
def historical_state_create_view(request, state_location_pk):
    state = State.objects.get(id=state_location_pk)
    form = HistoricalStateForm(request.POST or None, request.FILES or None, state_location_pk=state_location_pk)

    if request.htmx:
        template_name = 'platform_admin/historical/partials/historical-state-create.html'

    if form.is_valid():
        nigeria_as_country_location = Country.objects.get(id=1)

        form.instance.user = request.user.account_profile
        form.instance.country = nigeria_as_country_location
        form.instance.geo_political_zone = state.geo_political_zone
        form.instance.state = state
        newly_saved_form = form.save()
        # messages.success(request, "Data added successfully!!!")
        # return HttpResponseRedirect(reverse('platform_admin:market-sector-create-view'))

    context = {
    'form': form,
    'object': state,
    }
    return render(request, 'platform_admin/historical/historical-state-create.html', context)


@login_required
def historical_city_create_view(request, city_location_pk):
    city = City.objects.get(id=city_location_pk)
    form = HistoricalCityForm(request.POST or None, request.FILES or None, city_location_pk=city_location_pk)

    if request.htmx:
        template_name = 'platform_admin/historical/partials/historical-city-create.html'

    if form.is_valid():
        nigeria_as_country_location = Country.objects.get(id=1)

        form.instance.user = request.user.account_profile
        form.instance.country = nigeria_as_country_location
        form.instance.geo_political_zone = city.state.geo_political_zone
        form.instance.state = city.state
        form.instance.city = city
        newly_saved_form = form.save()
        # messages.success(request, "Data added successfully!!!")
        # return HttpResponseRedirect(reverse('platform_admin:market-sector-create-view'))

    context = {
    'form': form,
    'object': city,
    }
    return render(request, 'platform_admin/historical/historical-city-create.html', context)


@login_required
def historical_clan_create_view(request, clan_location_pk):
    clan = Clan.objects.get(id=clan_location_pk)
    form = HistoricalClanForm(request.POST or None, request.FILES or None)

    if request.htmx:
        template_name = 'platform_admin/historical/partials/historical-clan-create.html'

    if form.is_valid():
        nigeria_as_country_location = Country.objects.get(id=1)

        form.instance.user = request.user.account_profile
        form.instance.country = nigeria_as_country_location
        form.instance.geo_political_zone = clan.city.state.geo_political_zone
        form.instance.state = clan.city.state
        form.instance.city = clan.city
        form.instance.clan = clan
        newly_saved_form = form.save()
        # messages.success(request, "Data added successfully!!!")
        # return HttpResponseRedirect(reverse('platform_admin:market-sector-create-view'))

    context = {
    'form': form,
    'object': clan,
    }
    return render(request, 'platform_admin/historical/historical-clan-create.html', context)

################## END OF VARIOUS LOCATION DATA ENTRY CENTERS ###########################################




@login_required
def historical_data_list_view(request):
    geo_politicals = GeoPoliticalZone.objects.all().order_by('name')
    states = State.objects.all().order_by('name')
    cities = City.objects.all().order_by('name')
    categories = HistoricalCategory.objects.all().order_by('name')
    context = {
        'geo_politicals': geo_politicals,
        'states' : states,
        'cities' : cities,
        'categories': categories,
    }
    return render(request, 'platform_admin/historical/historical-data-list-view.html', context)


###################################### BEGINNING OF LOGGED IN USER HISTORICAL DATA ###########################################
@login_required
def user_historical_list_view(request):
    user_historicals = _load_user_historicals(request)
    # objects = MarketSector.objects.all().order_by('-date_created')
    context = {
        'user_historicals': user_historicals,
    }
    return render(request, 'platform_admin/historical/user-historicals.html', context)


@login_required
def list_load_user_historicals_view(request):
    user_historical = _load_user_historicals(request)
    context = {"user_historicals": user_historical,}
    return render(request, "platform_admin/historical/partials/user_historicals.html", context)

def _load_user_historicals(request):
    page = request.GET.get("page")
    user = request.user.account_profile
    user_historicals = Historical.objects.filter(user=user).order_by('-date_created')
    paginator = Paginator(user_historicals, 20)
    try:
        user_historicals = paginator.page(page)
    except PageNotAnInteger:
        user_historicals = paginator.page(1)
    except EmptyPage:
        user_historicals = paginator.page(paginator.num_pages)
    return user_historicals

###################################### END OF LOGGED IN USER HISTORICAL DATA ###########################################



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
    paginator = Paginator(historical_geo_zone_details, 20)
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
    paginator = Paginator(historical_state_location_details, 20)
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
    paginator = Paginator(historical_city_location_details, 20)
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
    paginator = Paginator(historical_clan_location_details, 20)
    try:
        historical_clan_location_details = paginator.page(page)
    except PageNotAnInteger:
        historical_clan_location_details = paginator.page(1)
    except EmptyPage:
        historical_clan_location_details = paginator.page(paginator.num_pages)
    return historical_clan_location_details

###################################### END OF CLANS LOCATION FOR HISTORICAL DATA ###########################################



###################################### BEGINNING OF Category FOR HISTORICAL DATA ###########################################

@login_required
def historical_category_detail_view(request, category_pk):
    object = HistoricalCategory.objects.get(id=category_pk)
    category_pk = category_pk
    objects = _load_historical_category_details(request, category_pk)
    context = {
        'object': object,
        'objects': objects,
    }
    return render(request, 'platform_admin/historical/historical-category-detail.html', context)



@login_required
def list_load_historical_category_details_view(request, category_pk):
    object = HistoricalCategory.objects.get(id=category_pk)
    historical_category_detail = _load_historical_category_details(request, category_pk)
    context = {"objects": historical_category_detail, 'object': object}
    return render(request, "platform_admin/historical/partials/historical_category_details.html", context)


@login_required
def _load_historical_category_details(request, category_pk):
    page = request.GET.get("page")
    historical_category_details = Historical.objects.filter(category=category_pk).order_by('-date_created')
    paginator = Paginator(historical_category_details, 20)
    try:
        historical_category_details = paginator.page(page)
    except PageNotAnInteger:
        historical_category_details = paginator.page(1)
    except EmptyPage:
        historical_category_details = paginator.page(paginator.num_pages)
    return historical_category_details

###################################### END OF Category FOR HISTORICAL DATA ###########################################