import django_filters

from app.apps.deals.models import RealtorInTheDeal, SubmittedCommission


class RealtorInTheDealFilter(django_filters.FilterSet):

    class Meta:
        model = RealtorInTheDeal
        fields = {
            'deal__id': ['in'],
        }

class SubmittedCommissionFilter(django_filters.FilterSet):

    class Meta:
        model = SubmittedCommission
        fields = {
            'deal__id': ['in'],
        }