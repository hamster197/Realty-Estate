from django.utils.translation import gettext_lazy as _

from django import forms
from django_select2.forms import ModelSelect2Widget, ModelSelect2TagWidget

from app.apps.real_estate.models import Commerce, Flat, House, PlotOfLand, CityQuide, DistrictQuide, Client


class RealtyEstateForm(forms.ModelForm):

    city = forms.ModelChoiceField(
        queryset=CityQuide.objects.all(),
        label=_("Город"),
        widget=ModelSelect2Widget(
            search_fields=["name__icontains"],
            max_results=500,
            attrs={"data-minimum-input-length": 0},
        ),
    )

    district = forms.ModelChoiceField(
        queryset=DistrictQuide.objects.all(),
        label=_("Район"),
        widget=ModelSelect2Widget(
            search_fields=["name__icontains"],
            dependent_fields={"city": "city"},
            max_results=500,
            attrs={"data-minimum-input-length": 0},
        ),
    )

    class Meta:
        model = None
        exclude = ('author', 'latitude', 'longitude', 'type', 'cadastral_number', )


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


class ClientNewForm(forms.ModelForm):

    city = forms.ModelChoiceField(
        queryset=CityQuide.objects.all(),
        label=_("Город"),
        widget=ModelSelect2Widget(
            search_fields=["name__icontains"],
            max_results=500,
            attrs={"data-minimum-input-length": 0},
        ),
    )

    district = forms.ModelMultipleChoiceField(
        queryset=DistrictQuide.objects.all(),
        label=_("Район"),
        widget=ModelSelect2TagWidget(
            search_fields=["name__icontains"],
            dependent_fields={"city": "city"},
            max_results=500,
            attrs={'style': 'width: 100%'},
        ),
    )

    class Meta:
        model = Client
        exclude = ['author', 'status',]
