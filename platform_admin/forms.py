from django import forms
from .models import MarketSector, MarketSectorBulkData
from utility.models import Country, State, City


class MarketSectorBulkDataForm(forms.ModelForm):
    state = forms.ModelChoiceField(
            label='State Location',
            widget=forms.Select,
            queryset=State.objects.all(),
        )


    city = forms.ModelChoiceField(
            label='City',
            widget=forms.Select,
            queryset=City.objects.all(),
        )
    class Meta:
        model = MarketSectorBulkData
        fields = ('filez', 'state', 'city')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['city'].queryset = City.objects.none()

        if 'state' in self.data:
            try:
                state_id = int(self.data.get('state'))
                self.fields['city'].queryset = City.objects.filter(state_id=state_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['city'].queryset = self.instance.state.city_set.order_by('name')


class MarketSectorForm(forms.ModelForm):
    state = forms.ModelChoiceField(
            label='State Location',
            widget=forms.Select,
            queryset=State.objects.all(),
        )


    city = forms.ModelChoiceField(
            label='City',
            widget=forms.Select,
            queryset=City.objects.all(),
        )
    class Meta:
        model = MarketSector
        fields = ['name', 'state', 'city', 'address_location',
                    'phone_number', 'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['city'].queryset = City.objects.none()

        if 'state' in self.data:
            try:
                state_id = int(self.data.get('state'))
                self.fields['city'].queryset = City.objects.filter(state_id=state_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['city'].queryset = self.instance.state.city_set.order_by('name')