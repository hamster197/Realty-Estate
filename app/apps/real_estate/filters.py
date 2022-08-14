import django_filters

from django_filters import ChoiceFilter, ModelChoiceFilter
from django_select2.forms import ModelSelect2Widget

from app.apps.real_estate.models import RealtyEstate, DistrictQuide, Flat, Commerce, PlotOfLand, House, CityQuide


class RealtyEstateFilter(django_filters.FilterSet):

    type = ChoiceFilter(choices=RealtyEstate.type_choises)

    district__city = ModelChoiceFilter(
        queryset=CityQuide.objects.all(),
        label="Город",
        widget=ModelSelect2Widget(
            search_fields=["name__icontains"],
            max_results=500,
            attrs={"data-minimum-input-length": 0},
        ),
    )

    district = ModelChoiceFilter(
        queryset=DistrictQuide.objects.all(),
        label="Район",
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

class MyAllRealtyEstateFilter(RealtyEstateFilter):

    @property
    def qs(self):
        parent = super(MyAllRealtyEstateFilter, self).qs
        author = getattr(self.request, 'user', None)
        return parent.filter(status_obj='Опубликован', author=author)

class MyFlatRealtyEstateFilter(MyAllRealtyEstateFilter):

    class Meta(MyAllRealtyEstateFilter.Meta):
        model = Flat

class MyHouseRealtyEstateFilter(RealtyEstateFilter):

    class Meta(MyAllRealtyEstateFilter.Meta):
        model = House

class MyPlotOfLandRealtyEstateFilter(MyAllRealtyEstateFilter):

    class Meta(MyAllRealtyEstateFilter.Meta):
        model = PlotOfLand

class MyCommerceRealtyEstateFilter(MyAllRealtyEstateFilter):

    class Meta(MyAllRealtyEstateFilter.Meta):
        model = Commerce
