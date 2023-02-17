from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from accounts.models import Account, Profile
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib import messages
from django.conf import settings
from .forms import MarketSectorForm, MarketSectorBulkDataForm
from .models import MarketSectorBulkData, MarketSector, Historical
from .tasks import create_new_customers
from utility.models import Country, State, GeoPoliticalZone, City, Clan
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.views.generic import ( ListView, DetailView, CreateView, 
                                    UpdateView, DeleteView, RedirectView, View, TemplateView)


@login_required
def market_sector_detail_view(request, pk):
    object = MarketSector.objects.get(id=pk)
    form = MarketSectorForm(request.POST or None, request.FILES or None, instance=object)

    if request.htmx:
        template_name = 'platform_admin/market_sector/partials/ajax_market_sector_update.html'

    if form.is_valid():
        # form.instance.user = request.user.account_profile
        form.save()
        messages.success(request, "Data added successfully!!!")
        return HttpResponseRedirect(reverse('platform_admin:market-sector-detail-view', kwargs={'pk': pk} ))

    context = {
        'object': object,
        'form': form,
    }
    return render(request, 'platform_admin/market_sector/market-sector-detail.html', context)

@login_required
def market_sector_list_view(request):
    market_sectors = _load_market_sectors(request)
    # objects = MarketSector.objects.all().order_by('-date_created')
    context = {
        'market_sectors': market_sectors,
    }
    return render(request, 'platform_admin/all-market-sectors.html', context)


@login_required
def list_load_market_sectors_view(request):
    market_sector = _load_market_sectors(request)
    context = {"market_sectors": market_sector,}
    return render(request, "platform_admin/partials/all-market_sectors.html", context)

def _load_market_sectors(request):
    page = request.GET.get("page")
    market_sectors = MarketSector.objects.all().order_by('-date_created')
    paginator = Paginator(market_sectors, 50)
    try:
        market_sectors = paginator.page(page)
    except PageNotAnInteger:
        market_sectors = paginator.page(1)
    except EmptyPage:
        market_sectors = paginator.page(paginator.num_pages)
    return market_sectors


@login_required
def market_sector_create_view(request):
    form = MarketSectorForm(request.POST or None, request.FILES or None)

    # if request.method == 'POST':
    #     form = MarketSectorForm(request.POST, request.FILES)
    #     if form.is_valid():
    #         form.instance.user = request.user.account_profile
    #         form.save()
    #         messages.success(request, "Data added successfully!!!")
    #         return HttpResponseRedirect(reverse('platform_admin:market-sector-create-view'))

    if request.htmx:
        template_name = 'platform_admin/market_sector/partials/ajax_market_sector_create.html'

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
    return render(request, 'platform_admin/market-sector-create.html', context)

@login_required
def market_sector_upload_view(request):
    form_bulk = MarketSectorBulkDataForm(request.POST or None, request.FILES or None)

    if request.htmx:
        template_name = 'platform_admin/ajax_progress_bar_upload.html'

    if form_bulk.is_valid():
        nigeria_as_country_location = Country.objects.get(id=1)

        form_bulk.instance.user = request.user.account_profile
        form_bulk.instance.country = nigeria_as_country_location
        newly_saved_form = form_bulk.save()
        messages.success(request, "We're still preparing your customers, refresh again after some seconds.")
        newly_saved_form_id = newly_saved_form.id

        user_profile_id = request.user.account_profile.id

        # Fuction that processes our csv and creates customers
        # create_new_customers.delay(newly_saved_form_id, user_profile_id)
        create_new_customers(newly_saved_form_id, user_profile_id)

    context = {
        'form_bulk': form_bulk,
    }
    return render(request, 'platform_admin/market-sector-upload.html', context)





@login_required
def market_sector_data_list_view(request):
    geo_politicals = GeoPoliticalZone.objects.all().order_by('name')
    states = State.objects.all().order_by('name')
    cities = City.objects.all().order_by('name')
    context = {
        'geo_politicals': geo_politicals,
        'states' : states,
        'cities' : cities,
    }
    return render(request, 'platform_admin/market_sector/market_sector-data-list-view.html', context)


###################################### BEGINNING OF GEOPOLITICAL ZONES FOR MARKET_SECTOR DATA ###########################################
@login_required
def market_sector_geo_zone_detail_view(request, geozone_pk):
    object = GeoPoliticalZone.objects.get(id=geozone_pk)
    geozone_pk = geozone_pk
    objects = _load_market_sector_geo_zone_details(request, geozone_pk)
    context = {
        'object': object,
        'objects': objects,
        'states': State.objects.filter(geo_political_zone=object).order_by('name'),
    }
    return render(request, 'platform_admin/market_sector/market_sector-geo-zone-detail.html', context)



@login_required
def list_load_market_sector_geo_zone_details_view(request, geozone_pk):
    object = GeoPoliticalZone.objects.get(id=geozone_pk)
    market_sector_geo_zone_detail = _load_market_sector_geo_zone_details(request, geozone_pk)
    context = {"objects": market_sector_geo_zone_detail, 'object': object}
    return render(request, "platform_admin/market_sector/partials/market_sector_geo_zone_details.html", context)



@login_required
def _load_market_sector_geo_zone_details(request, geozone_pk):
    page = request.GET.get("page")
    market_sector_geo_zone_details = MarketSector.objects.filter(geo_political_zone=geozone_pk).order_by('-date_created')
    paginator = Paginator(market_sector_geo_zone_details, 1)
    try:
        market_sector_geo_zone_details = paginator.page(page)
    except PageNotAnInteger:
        market_sector_geo_zone_details = paginator.page(1)
    except EmptyPage:
        market_sector_geo_zone_details = paginator.page(paginator.num_pages)
    return market_sector_geo_zone_details

###################################### END OF GEOPOLITICAL ZONES FOR MARKET_SECTOR DATA ###########################################



###################################### BEGINNING OF STATES LOCATION FOR MARKET_SECTOR DATA ###########################################


@login_required
def market_sector_state_location_detail_view(request, state_location_pk):
    object = State.objects.get(id=state_location_pk)
    state_location_pk = state_location_pk
    objects = _load_market_sector_state_location_details(request, state_location_pk)
    context = {
        'object': object,
        'objects': objects,
        'cities': City.objects.filter(state=object).order_by('name'),
    }
    return render(request, 'platform_admin/market_sector/market_sector-state-location-detail.html', context)



@login_required
def list_load_market_sector_state_location_details_view(request, state_location_pk):
    object = State.objects.get(id=state_location_pk)
    market_sector_state_location_detail = _load_market_sector_state_location_details(request, state_location_pk)
    context = {"objects": market_sector_state_location_detail, 'object': object}
    return render(request, "platform_admin/market_sector/partials/market_sector_state_location_details.html", context)



@login_required
def _load_market_sector_state_location_details(request, state_location_pk):
    page = request.GET.get("page")
    market_sector_state_location_details = MarketSector.objects.filter(state=state_location_pk).order_by('-date_created')
    paginator = Paginator(market_sector_state_location_details, 1)
    try:
        market_sector_state_location_details = paginator.page(page)
    except PageNotAnInteger:
        market_sector_state_location_details = paginator.page(1)
    except EmptyPage:
        market_sector_state_location_details = paginator.page(paginator.num_pages)
    return market_sector_state_location_details

###################################### END OF STATES LOCATION FOR MARKET_SECTOR DATA ###########################################




###################################### BEGINNING OF CITIES LOCATION FOR MARKET_SECTOR DATA ###########################################


@login_required
def market_sector_city_location_detail_view(request, city_location_pk):
    object = City.objects.get(id=city_location_pk)
    city_location_pk = city_location_pk
    objects = _load_market_sector_city_location_details(request, city_location_pk)
    context = {
        'object': object,
        'objects': objects,
        'clans': Clan.objects.filter(city=object).order_by('name'),
    }
    return render(request, 'platform_admin/market_sector/market_sector-city-location-detail.html', context)



@login_required
def list_load_market_sector_city_location_details_view(request, city_location_pk):
    object = City.objects.get(id=city_location_pk)
    market_sector_city_location_detail = _load_market_sector_city_location_details(request, city_location_pk)
    context = {"objects": market_sector_city_location_detail, 'object': object}
    return render(request, "platform_admin/market_sector/partials/market_sector_city_location_details.html", context)



@login_required
def _load_market_sector_city_location_details(request, city_location_pk):
    page = request.GET.get("page")
    market_sector_city_location_details = MarketSector.objects.filter(city=city_location_pk).order_by('-date_created')
    paginator = Paginator(market_sector_city_location_details, 1)
    try:
        market_sector_city_location_details = paginator.page(page)
    except PageNotAnInteger:
        market_sector_city_location_details = paginator.page(1)
    except EmptyPage:
        market_sector_city_location_details = paginator.page(paginator.num_pages)
    return market_sector_city_location_details

###################################### END OF CITIES LOCATION FOR MARKET_SECTOR DATA ###########################################




###################################### BEGINNING OF CLANS LOCATION FOR MARKET_SECTOR DATA ###########################################


@login_required
def market_sector_clan_location_detail_view(request, clan_location_pk):
    object = Clan.objects.get(id=clan_location_pk)
    clan_location_pk = clan_location_pk
    objects = _load_market_sector_clan_location_details(request, clan_location_pk)
    context = {
        'object': object,
        'objects': objects,
    }
    return render(request, 'platform_admin/market_sector/market_sector-clan-location-detail.html', context)



@login_required
def list_load_market_sector_clan_location_details_view(request, clan_location_pk):
    object = Clan.objects.get(id=clan_location_pk)
    market_sector_clan_location_detail = _load_market_sector_clan_location_details(request, clan_location_pk)
    context = {"objects": market_sector_clan_location_detail, 'object': object}
    return render(request, "platform_admin/market_sector/partials/market_sector_clan_location_details.html", context)



@login_required
def _load_market_sector_clan_location_details(request, clan_location_pk):
    page = request.GET.get("page")
    market_sector_clan_location_details = MarketSector.objects.filter(clan=clan_location_pk).order_by('-date_created')
    paginator = Paginator(market_sector_clan_location_details, 1)
    try:
        market_sector_clan_location_details = paginator.page(page)
    except PageNotAnInteger:
        market_sector_clan_location_details = paginator.page(1)
    except EmptyPage:
        market_sector_clan_location_details = paginator.page(paginator.num_pages)
    return market_sector_clan_location_details

###################################### END OF CLANS LOCATION FOR MARKET_SECTOR DATA ###########################################
