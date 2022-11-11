from django.utils.translation import gettext_lazy as _


import django_filters

from django_filters import ChoiceFilter, ModelChoiceFilter
from django_select2.forms import ModelSelect2Widget

from app.apps.real_estate.models import RealtyEstate, DistrictQuide, Flat, Commerce, PlotOfLand, House, CityQuide, \
    Client

class RealtyEstateFilter(django_filters.FilterSet):
    type = ChoiceFilter(choices=RealtyEstate.type_choises)
    district__city = ModelChoiceFilter(
        queryset=CityQuide.objects.all(),
        label=_("Город"),
        widget=ModelSelect2Widget(
            search_fields=["name__icontains"],
            max_results=500,
            attrs={"data-minimum-input-length": 0},
        ),
    )
    district = ModelChoiceFilter(
        queryset=DistrictQuide.objects.all(),
        label=_("Район"),
        widget=ModelSelect2Widget(
            search_fields=["name__icontains"],
            dependent_fields={"district__city": "city"},
            max_results=500,
            attrs={"data-minimum-input-length": 0},
        ),
    )

    class Meta:
        model = RealtyEstate
        fields = {
            'type': [],
            'district': [],
            'agency_price': ['lte', 'gte'],
        }
    @property
    def qs(self):
        parent = super(RealtyEstateFilter, self).qs
        return parent.filter(status_obj='Опубликован')

class MyFlatRealtyEstateFilter(django_filters.FilterSet):

    district__city = ModelChoiceFilter(
        queryset=CityQuide.objects.all(),
        label=_("Город"),
        widget=ModelSelect2Widget(
            search_fields=["name__icontains"],
            max_results=500,
            attrs={"data-minimum-input-length": 0},
        ),
    )
    district = ModelChoiceFilter(
        queryset=DistrictQuide.objects.all(),
        label=_("Район"),
        widget=ModelSelect2Widget(
            search_fields=["name__icontains"],
            dependent_fields={"district__city": "city"},
            max_results=500,
            attrs={"data-minimum-input-length": 0},
        ),
    )
    class Meta:
        model = Flat
        fields = {
            'agency_price': ['lte', 'gte'],
        }
    @property
    def qs(self):
        parent = super(MyFlatRealtyEstateFilter, self).qs
        author = getattr(self.request, 'user', None)
        return parent.filter(status_obj='Опубликован', author=author, )

class MyHouseRealtyEstateFilter(MyFlatRealtyEstateFilter):

    class Meta(MyFlatRealtyEstateFilter.Meta):
        model = House

class MyPlotOfLandRealtyEstateFilter(MyFlatRealtyEstateFilter):
    class Meta(MyFlatRealtyEstateFilter.Meta):
        model = PlotOfLand

class MyCommerceRealtyEstateFilter(MyFlatRealtyEstateFilter):

    class Meta(MyFlatRealtyEstateFilter.Meta):
        model = Commerce

class AllClientEstateFilter(django_filters.FilterSet):
    estate_type = ChoiceFilter(choices=RealtyEstate.type_choises)
    district__city = ModelChoiceFilter(
        queryset=CityQuide.objects.all(),
        label=_("Город"),
        widget=ModelSelect2Widget(
            search_fields=["name__icontains"],
            max_results=500,
            attrs={"data-minimum-input-length": 0},
        ),
    )
    district = ModelChoiceFilter(
        queryset=DistrictQuide.objects.all(),
        label=_("Район"),
        widget=ModelSelect2Widget(
            search_fields=["name__icontains"],
            dependent_fields={"district__city": "city"},
            max_results=500,
            attrs={"data-minimum-input-length": 0},
        ),
    )
    class Meta:
        model = Client
        fields = {
            'estate_type': [],
            'district': [],
            'max_price': ['lte', 'gte'],
        }
    @property
    def qs(self):
        parent = super(AllClientEstateFilter, self).qs
        return parent.filter(status=False)

class MyClientEstateFilter(AllClientEstateFilter):
    @property
    def qs(self):
        parent = super(AllClientEstateFilter, self).qs
        author = getattr(self.request, 'user', None)
        return parent.filter(status=False, author=author,)
