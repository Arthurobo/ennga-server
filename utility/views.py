from django.shortcuts import render

from .models import Country, State, City, Clan
from accounts.models import Profile
                        

def load_states(request):
    geo_political_zone_id = request.GET.get('geo_political_zone')
    states = State.objects.filter(geo_political_zone_id=geo_political_zone_id).order_by('name')
    return render(request, 'utility/state_dropdown_list_options.html', {'states': states})
                        

def load_cities(request):
    state_id = request.GET.get('state')
    cities = City.objects.filter(state_id=state_id).order_by('name')
    return render(request, 'utility/city_dropdown_list_options.html', {'cities': cities})


def load_clans(request):
    city_id = request.GET.get('city')
    clans = Clan.objects.filter(city_id=city_id).order_by('name')
    return render(request, 'utility/clan_dropdown_list_options.html', {'clans': clans})
