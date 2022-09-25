import django_filters
from django_filters import ModelChoiceFilter

from app.apps.real_estate.models import RealtyEstate, House, Flat, DistrictQuide, PlotOfLand, Commerce, Client


class DrfRealtyEstateFilter(django_filters.FilterSet):
    district = ModelChoiceFilter(
        queryset=DistrictQuide.objects.all(),
        label="Район",
    )

    class Meta:
        model = RealtyEstate
        fields = {
            'district': [],
            'agency_price': ['lte', 'gte'],
        }

    @property
    def qs(self):
        parent = super(DrfRealtyEstateFilter, self).qs
        author = getattr(self.request, 'user', None)
        return parent.filter(status_obj='Опубликован', author=author,)

class DrfMyFlatRealtyEstateFilter(DrfRealtyEstateFilter):

    class Meta(DrfRealtyEstateFilter.Meta):
        model = Flat

class DrfMyHouseRealtyEstateFilter(DrfRealtyEstateFilter):

    class Meta(DrfRealtyEstateFilter.Meta):
        model = House

class DrfMyPlotOfLandRealtyEstateFilter(DrfRealtyEstateFilter):

    class Meta(DrfRealtyEstateFilter.Meta):
        model = PlotOfLand

class DrfMyCommerceRealtyEstateFilter(DrfRealtyEstateFilter):

    class Meta(DrfRealtyEstateFilter.Meta):
        model = Commerce

class MyClientFilter(django_filters.FilterSet):
    district = ModelChoiceFilter(
        queryset=DistrictQuide.objects.all(),
        label="Район",
    )
    class Meta:
        model = Client
        fields = {
            'district': [],
            'max_price': ['lte', 'gte'],
        }
    @property
    def qs(self):
        parent = super(MyClientFilter, self).qs
        author = getattr(self.request, 'user', None)
        return parent.filter(author=author, status=False)

class AllClientFilter(django_filters.FilterSet):
    @property
    def qs(self):
        parent = super(AllClientFilter, self).qs
        author = getattr(self.request, 'user', None)
        return parent.filter(status=False).exclude(author=author)