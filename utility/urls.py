from django.urls import path
from .views import (
                    load_states, load_cities,
)

app_name = "utility"


urlpatterns = [
    path('ajax/load-states/', load_states, name='ajax-load-states'),
    path('ajax/load-cities/', load_cities, name='ajax-load-cities'),
]