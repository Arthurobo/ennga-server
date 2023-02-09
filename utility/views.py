from django.shortcuts import render

from .models import Country, State, City
from accounts.models import Profile
                        

def load_states(request):
    country_id = request.GET.get('country')
    states = State.objects.filter(country_id=country_id).order_by('name')
    return render(request, 'utility/state_dropdown_list_options.html', {'states': states})

def load_cities(request):
    state_id = request.GET.get('state')
    cities = City.objects.filter(state_id=state_id).order_by('name')
    return render(request, 'utility/city_dropdown_list_options.html', {'cities': cities})