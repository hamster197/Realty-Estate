from django import forms
from django_select2.forms import ModelSelect2Widget

from app.apps.real_estate.models import Commerce, Flat, House, PlotOfLand, CityQuide, DistrictQuide

class RealtyEstateForm(forms.ModelForm):

    city = forms.ModelChoiceField(
        queryset=CityQuide.objects.all(),
        label="Город",
        widget=ModelSelect2Widget(
            search_fields=["name__icontains"],
            max_results=500,
            attrs={"data-minimum-input-length": 0},
        ),
    )

    district = forms.ModelChoiceField(
        queryset=DistrictQuide.objects.all(),
        label="Район",
        widget=ModelSelect2Widget(
            search_fields=["name__icontains"],
            dependent_fields={"city": "city"},
            max_results=500,
            attrs={"data-minimum-input-length": 0},
        ),
    )

    class Meta:
        model = None
        exclude = ('author', 'latitude', 'longitude', 'type', 'latitude', 'longitude',)

class FlatEditForm(RealtyEstateForm):

    class Meta(RealtyEstateForm.Meta):
        model = Flat

class HouseEditForm(RealtyEstateForm):

    class Meta(RealtyEstateForm.Meta):
        model = House


class PlotOfLandEditForm(RealtyEstateForm):

    class Meta(RealtyEstateForm.Meta):
        model = PlotOfLand


class CommerceEditForm(RealtyEstateForm):

    class Meta(RealtyEstateForm.Meta):
        model = Commerce

