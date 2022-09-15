from django.db.models import Count

from app.apps.deals.models import Deal


def OpenDealList(user, deal_status):

    if user.groups.count() == 0:
        return Deal.objects.none()

    elif user.groups.get().name == 'Генеральный директор':
        return Deal.objects.filter(status__in=deal_status, )

    elif user.groups.get().name == 'Начальник филиала':
        return Deal.objects.filter(status__in=deal_status,
                                   realtor_in_deal_deal_id__name__departament__city=user.departament.city).annotate(
            Count('pk'))

    elif user.department_boss:
        department = []
        department.append(user.departament)
        return Deal.objects.filter(status__in=deal_status,
                                   realtor_in_deal_deal_id__name__departament__in=department).annotate(Count('pk'))

    elif user.groups.get().name == 'Риелтор':
        return Deal.objects.filter(status__in=deal_status, realtor_in_deal_deal_id__name=user)