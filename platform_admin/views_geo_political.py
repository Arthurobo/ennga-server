from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from accounts.models import Account
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib import messages

from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from accounts.forms import (RegistrationForm, AccountAuthenticationForm, 
                            AccountUpdateForm, UserProfileUpdateForm)
from accounts.models import Account, Profile
from django.conf import settings
from .forms import MarketSectorForm, MarketSectorBulkDataForm
from .models import MarketSectorBulkData, MarketSector
from .tasks import create_new_customers
from utility.models import Country

from django.shortcuts import render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

# Create your views here.


def geo_political_list_view(request, pk):
    geo_politicals = _load_geo_politicals(request)
    # objects = MarketSector.objects.all().order_by('-date_created')
    context = {
        'geo_politicals': geo_politicals,
    }
    return render(request, 'platform_admin/all-geo-politicals.html', context)


def list_load_geo_politicals_view(request):
    geo_political = _load_geo_politicals(request)
    context = {"geo_politicals": geo_political,}
    return render(request, "platform_admin/partials/all-geo_politicals.html", context)


def _load_geo_politicals(request):
    page = request.GET.get("page")
    geo_politicals = MarketSector.objects.all().order_by('-date_created')
    paginator = Paginator(geo_politicals, 50)
    try:
        geo_politicals = paginator.page(page)
    except PageNotAnInteger:
        geo_politicals = paginator.page(1)
    except EmptyPage:
        geo_politicals = paginator.page(paginator.num_pages)
    return geo_politicals



def geo_political_create_view(request):
    form = MarketSectorForm()

    if request.method == 'POST':
        form = MarketSectorForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.user = request.user.account_profile
            form.save()
            messages.success(request, "Data added successfully!!!")
            return HttpResponseRedirect(reverse('platform_admin:geo-political-create-view'))

    context = {
        'form': form,
    }
    return render(request, 'platform_admin/geo-political-create.html', context)


def geo_political_upload_view(request):
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
    return render(request, 'platform_admin/geo-political-upload.html', context)