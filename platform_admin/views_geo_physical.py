from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from accounts.models import Account, Profile
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib import messages
from django.conf import settings
from .forms import MarketSectorForm, MarketSectorBulkDataForm, GeoPhysicalForm
from .models import MarketSectorBulkData, MarketSector, Historical, GeoPhysicalData
from .tasks import create_new_customers
from utility.models import Country, State, GeoPoliticalZone, City, Clan
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.views.generic import ( ListView, DetailView, CreateView, 
                                    UpdateView, DeleteView, RedirectView, View, TemplateView)


@login_required
def geo_physical_detail_view(request, pk):
    object = GeoPhysicalData.objects.get(id=pk)
    form = GeoPhysicalForm(request.POST or None, request.FILES or None, instance=object)

    if request.htmx:
        template_name = 'platform_admin/geo_physical/partials/ajax_geo_physical_update.html'

    if form.is_valid():
        # form.instance.user = request.user.account_profile
        form.save()
        messages.success(request, "Data added successfully!!!")
        return HttpResponseRedirect(reverse('platform_admin:geo-physical-detail-view', kwargs={'pk': pk} ))

    context = {
        'object': object,
        'form': form,
    }
    return render(request, 'platform_admin/geo_physical/geo-physical-detail.html', context)



@login_required
def geo_physical_list_view(request):
    geo_physicals = _load_geo_physicals(request)
    # objects = MarketSector.objects.all().order_by('-date_created')
    context = {
        'geo_physicals': geo_physicals,
    }
    return render(request, 'platform_admin/geo_physical/all-geo-physicals.html', context)


@login_required
def list_load_geo_physicals_view(request):
    geo_physical = _load_geo_physicals(request)
    context = {"geo_physicals": geo_physical,}
    return render(request, "platform_admin/geo_physical/partials/all-geo-physicals.html", context)

def _load_geo_physicals(request):
    page = request.GET.get("page")
    geo_physicals = GeoPhysicalData.objects.all().order_by('-date_created')
    paginator = Paginator(geo_physicals, 20)
    try:
        geo_physicals = paginator.page(page)
    except PageNotAnInteger:
        geo_physicals = paginator.page(1)
    except EmptyPage:
        geo_physicals = paginator.page(paginator.num_pages)
    return geo_physicals



@login_required
def geo_physical_create_view(request):
    form = GeoPhysicalForm(request.POST or None, request.FILES or None)

    if request.htmx:
        template_name = 'platform_admin/geo_physical/partials/ajax_geo_physical_create.html'

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
    return render(request, 'platform_admin/geo_physical/geo-physical-create.html', context)


@login_required
def geo_physical_data_list_view(request):
    geo_politicals = GeoPoliticalZone.objects.all().order_by('name')
    states = State.objects.all().order_by('name')
    cities = City.objects.all().order_by('name')
    context = {
        'geo_politicals': geo_politicals,
        'states' : states,
        'cities' : cities,
    }
    return render(request, 'platform_admin/geo_physical/geo_physical-data-list-view.html', context)





###################################### BEGINNING OF LOGGED IN USER GEO_PHYSICAL DATA ###########################################
@login_required
def user_geo_physical_list_view(request):
    user_geo_physicals = _load_user_geo_physicals(request)
    # objects = MarketSector.objects.all().order_by('-date_created')
    context = {
        'user_geo_physicals': user_geo_physicals,
    }
    return render(request, 'platform_admin/geo_physical/user-geo-physicals.html', context)


@login_required
def list_load_user_geo_physicals_view(request):
    user_geo_physical = _load_user_geo_physicals(request)
    context = {"user_geo_physicals": user_geo_physical,}
    return render(request, "platform_admin/geo_physical/partials/user_geo_physicals.html", context)

def _load_user_geo_physicals(request):
    page = request.GET.get("page")
    user = request.user.account_profile
    user_geo_physicals = GeoPhysicalData.objects.filter(user=user).order_by('-date_created')
    paginator = Paginator(user_geo_physicals, 20)
    try:
        user_geo_physicals = paginator.page(page)
    except PageNotAnInteger:
        user_geo_physicals = paginator.page(1)
    except EmptyPage:
        user_geo_physicals = paginator.page(paginator.num_pages)
    return user_geo_physicals

###################################### END OF LOGGED IN USER GEO_PHYSICAL DATA ###########################################




###################################### BEGINNING OF GEOPOLITICAL ZONES FOR GEO_PHYSICAL DATA ###########################################
@login_required
def geo_physical_geo_zone_detail_view(request, geozone_pk):
    object = GeoPoliticalZone.objects.get(id=geozone_pk)
    geozone_pk = geozone_pk
    objects = _load_geo_physical_geo_zone_details(request, geozone_pk)
    context = {
        'object': object,
        'objects': objects,
        'states': State.objects.filter(geo_political_zone=object).order_by('name'),
    }
    return render(request, 'platform_admin/geo_physical/geo_physical-geo-zone-detail.html', context)



@login_required
def list_load_geo_physical_geo_zone_details_view(request, geozone_pk):
    object = GeoPoliticalZone.objects.get(id=geozone_pk)
    geo_physical_geo_zone_detail = _load_geo_physical_geo_zone_details(request, geozone_pk)
    context = {"objects": geo_physical_geo_zone_detail, 'object': object}
    return render(request, "platform_admin/geo_physical/partials/geo_physical_geo_zone_details.html", context)



@login_required
def _load_geo_physical_geo_zone_details(request, geozone_pk):
    page = request.GET.get("page")
    geo_physical_geo_zone_details = GeoPhysicalData.objects.filter(geo_political_zone=geozone_pk).order_by('-date_created')
    paginator = Paginator(geo_physical_geo_zone_details, 20)
    try:
        geo_physical_geo_zone_details = paginator.page(page)
    except PageNotAnInteger:
        geo_physical_geo_zone_details = paginator.page(1)
    except EmptyPage:
        geo_physical_geo_zone_details = paginator.page(paginator.num_pages)
    return geo_physical_geo_zone_details

###################################### END OF GEOPOLITICAL ZONES FOR GEO_PHYSICAL DATA ###########################################


###################################### BEGINNING OF STATES LOCATION FOR GEO_PHYSICAL DATA ###########################################
@login_required
def geo_physical_state_location_detail_view(request, state_location_pk):
    object = State.objects.get(id=state_location_pk)
    state_location_pk = state_location_pk
    objects = _load_geo_physical_state_location_details(request, state_location_pk)
    context = {
        'object': object,
        'objects': objects,
        'cities': City.objects.filter(state=object).order_by('name'),
    }
    return render(request, 'platform_admin/geo_physical/geo_physical-state-location-detail.html', context)



@login_required
def list_load_geo_physical_state_location_details_view(request, state_location_pk):
    object = State.objects.get(id=state_location_pk)
    geo_physical_state_location_detail = _load_geo_physical_state_location_details(request, state_location_pk)
    context = {"objects": geo_physical_state_location_detail, 'object': object}
    return render(request, "platform_admin/geo_physical/partials/geo_physical_state_location_details.html", context)



@login_required
def _load_geo_physical_state_location_details(request, state_location_pk):
    page = request.GET.get("page")
    geo_physical_state_location_details = GeoPhysicalData.objects.filter(state=state_location_pk).order_by('-date_created')
    paginator = Paginator(geo_physical_state_location_details, 20)
    try:
        geo_physical_state_location_details = paginator.page(page)
    except PageNotAnInteger:
        geo_physical_state_location_details = paginator.page(1)
    except EmptyPage:
        geo_physical_state_location_details = paginator.page(paginator.num_pages)
    return geo_physical_state_location_details

###################################### END OF STATES LOCATION FOR GEO_PHYSICAL DATA ###########################################



###################################### BEGINNING OF CITIES LOCATION FOR GEO_PHYSICAL DATA ###########################################

@login_required
def geo_physical_city_location_detail_view(request, city_location_pk):
    object = City.objects.get(id=city_location_pk)
    city_location_pk = city_location_pk
    objects = _load_geo_physical_city_location_details(request, city_location_pk)
    context = {
        'object': object,
        'objects': objects,
        'clans': Clan.objects.filter(city=object).order_by('name'),
    }
    return render(request, 'platform_admin/geo_physical/geo_physical-city-location-detail.html', context)



@login_required
def list_load_geo_physical_city_location_details_view(request, city_location_pk):
    object = City.objects.get(id=city_location_pk)
    geo_physical_city_location_detail = _load_geo_physical_city_location_details(request, city_location_pk)
    context = {"objects": geo_physical_city_location_detail, 'object': object}
    return render(request, "platform_admin/geo_physical/partials/geo_physical_city_location_details.html", context)



@login_required
def _load_geo_physical_city_location_details(request, city_location_pk):
    page = request.GET.get("page")
    geo_physical_city_location_details = GeoPhysicalData.objects.filter(city=city_location_pk).order_by('-date_created')
    paginator = Paginator(geo_physical_city_location_details, 20)
    try:
        geo_physical_city_location_details = paginator.page(page)
    except PageNotAnInteger:
        geo_physical_city_location_details = paginator.page(1)
    except EmptyPage:
        geo_physical_city_location_details = paginator.page(paginator.num_pages)
    return geo_physical_city_location_details

###################################### END OF CITIES LOCATION FOR GEO_PHYSICAL DATA ###########################################


###################################### BEGINNING OF CLANS LOCATION FOR GEO_PHYSICAL DATA ###########################################


@login_required
def geo_physical_clan_location_detail_view(request, clan_location_pk):
    object = Clan.objects.get(id=clan_location_pk)
    clan_location_pk = clan_location_pk
    objects = _load_geo_physical_clan_location_details(request, clan_location_pk)
    context = {
        'object': object,
        'objects': objects,
    }
    return render(request, 'platform_admin/geo_physical/geo_physical-clan-location-detail.html', context)



@login_required
def list_load_geo_physical_clan_location_details_view(request, clan_location_pk):
    object = Clan.objects.get(id=clan_location_pk)
    geo_physical_clan_location_detail = _load_geo_physical_clan_location_details(request, clan_location_pk)
    context = {"objects": geo_physical_clan_location_detail, 'object': object}
    return render(request, "platform_admin/geo_physical/partials/geo_physical_clan_location_details.html", context)



@login_required
def _load_geo_physical_clan_location_details(request, clan_location_pk):
    page = request.GET.get("page")
    geo_physical_clan_location_details = GeoPhysicalData.objects.filter(clan=clan_location_pk).order_by('-date_created')
    paginator = Paginator(geo_physical_clan_location_details, 20)
    try:
        geo_physical_clan_location_details = paginator.page(page)
    except PageNotAnInteger:
        geo_physical_clan_location_details = paginator.page(1)
    except EmptyPage:
        geo_physical_clan_location_details = paginator.page(paginator.num_pages)
    return geo_physical_clan_location_details

###################################### END OF CLANS LOCATION FOR GEO_PHYSICAL DATA ###########################################
