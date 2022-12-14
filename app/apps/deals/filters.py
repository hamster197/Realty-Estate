import django_filters
from django_filters import DateFromToRangeFilter
from django_filters.widgets import RangeWidget
from django.utils import timezone

from app.apps.deals.models import Deal


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



