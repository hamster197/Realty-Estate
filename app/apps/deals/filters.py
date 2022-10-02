import django_filters
from django_filters import DateFromToRangeFilter, ModelChoiceFilter
from django_filters.widgets import RangeWidget
from django.utils import timezone
from django.db.models import Sum

from app.apps.accounts.models import Departament
from app.apps.deals.models import Deal, RealtorInTheDeal
from app.apps.real_estate.models import CityQuide


class DealFilterMixin(django_filters.FilterSet):
    date_close_deal = DateFromToRangeFilter(widget=RangeWidget(attrs={'class': 'datepicker', 'type': 'date', }), )

    class Meta:
        model = Deal
        fields = {
        }

    @property
    def qs(self):
        parent = super().qs
        if not self.is_valid():
            start_date = timezone.now().replace(hour=0, minute=0, second=0, day=1)
            end_date = timezone.now().replace(hour=23, minute=59, second=59)
            field_name = "date_close_deal"
            lookup_gte = "%s__gte" % (field_name)
            lookup_lte = "%s__lte" % (field_name)
            kwargs = {lookup_gte: start_date, lookup_lte: end_date}
            author = getattr(self.request, 'user', None)

            if author.groups.count() == 0:
                return parent.none()

            elif author.groups.get().name == 'Генеральный директор':
                return parent.filter(**kwargs)

            elif author.groups.get().name == 'Начальник филиала':
                return parent.filter(**kwargs, realtor_in_deal_deal_id__name__departament__city=author.departament.city)

            elif author.department_boss:
                department = []
                department.append(author.departament,)
                return parent.filter(**kwargs, realtor_in_deal_deal_id__name__departament__in=department)

            elif author.groups.get().name == 'Риелтор':
                return parent.filter(**kwargs, realtor_in_deal_deal_id__name=author)
        else:
            return parent

class DealClosedFilter(DealFilterMixin):

    @property
    def qs(self):
        parent = super(DealClosedFilter, self).qs
        return parent.filter(status='Закрыта',)

class DealInstallmentClosedFilter(DealFilterMixin):

    @property
    def qs(self):
        parent = super(DealInstallmentClosedFilter, self).qs
        return parent.filter(status='Закрыта-Рассрочка',)

class DealDisruptionFilter(DealFilterMixin):

    @property
    def qs(self):
        parent = super(DealDisruptionFilter, self).qs
        return parent.filter(status='Срыв',)

class DealReitingFilterMixin(django_filters.FilterSet):
    deal__date_close_deal = DateFromToRangeFilter(widget=RangeWidget(attrs={'class': 'datepicker', 'type': 'date', }), )

    class Meta:
        model = RealtorInTheDeal
        fields = {}

    @property
    def qs(self, ):
        parent = super(DealReitingFilterMixin, self).qs
        if not self.is_valid():
            start_date = timezone.now().replace(hour=0, minute=0, second=0, day=1)
            end_date = timezone.now().replace(hour=23, minute=59, second=59)
            field_name = "deal__date_close_deal"
            lookup_gte = "%s__gte" % (field_name)
            lookup_lte = "%s__lte" % (field_name)
            kwargs = {lookup_gte: start_date, lookup_lte: end_date}
            return parent.filter(**kwargs, deal__status='Закрыта',).annotate(commision=Sum('realtor_commision_sum',))\
                .order_by('-commision')

        else:
            return parent.annotate(commision=Sum('realtor_commision_sum',)).order_by('-commision')


class DealDepartmentReitingFilter(DealReitingFilterMixin):
    name__departament = ModelChoiceFilter(queryset=Departament.objects.all().distinct(), to_field_name='pk',
                                                empty_label='All departments', label='department', )

    class Meta:
        model = RealtorInTheDeal
        fields = {}

class DealCityReitingFilter(DealReitingFilterMixin):
    name__departament__city = ModelChoiceFilter(queryset=CityQuide.objects.all().distinct(), to_field_name='pk',
                                                empty_label='All citys', label='city', )

    class Meta:
        model = RealtorInTheDeal
        fields = {}


