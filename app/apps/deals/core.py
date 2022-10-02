from django.db.models import Count, Sum
from django.shortcuts import get_object_or_404

from app.apps.deals.models import Deal, DealSystemQuide


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

def AllDealsCounter(start_date, end_date):
    rezult_string = 'Open deals '
    status_deal = ['Открыта', 'Рассрочка']
    all_open_deals = Deal.objects.filter(status__in=status_deal)
    all_closed_deals = Deal.objects.filter(date_close_deal__gte=start_date, date_close_deal__lte=end_date) \
        .exclude(status__in=status_deal)

    agence_percent = 100 - get_object_or_404(DealSystemQuide, pk=1).agency_commision_percent

    if all_open_deals.filter(status='Открыта').count():
        commision = (all_open_deals.filter(status='Открыта').aggregate(commision=Sum('commission', ))['commision'] * \
                 agence_percent) / 100
    else:
        commision = 0
    rezult_string = rezult_string + str(all_open_deals.filter(status='Открыта').count()) + ' / ' + str(commision)

    if all_open_deals.filter(status='Рассрочка').exists():
        commision = (all_open_deals.filter(status='Рассрочка').aggregate(commision=Sum('commission', ))['commision'] * \
                 agence_percent) / 100
    else:
        commision = 0

    rezult_string = rezult_string + ' Installment '
    rezult_string = rezult_string + str(all_open_deals.filter(status='Рассрочка').count()) + ' / ' + str(commision)

    if all_closed_deals.filter(status='Закрыта').exists():
        commision = (all_closed_deals.filter(status='Закрыта').aggregate(commision=Sum('commission', ))['commision'] * \
                 agence_percent) / 100
    else:
        commision = 0
    rezult_string = rezult_string + ' Closed '
    rezult_string = rezult_string + str(all_closed_deals.filter(status='Закрыта').count()) + ' / ' + str(commision)

    if all_closed_deals.filter(status='Закрыта-Рассрочка').exists():
        commision = (all_closed_deals.filter(status='Закрыта-Рассрочка')
                     .aggregate(commision=Sum('commission', ))['commision'] * \
                 agence_percent) / 100
    else:
        commision = 0
    rezult_string = rezult_string + ' closed_installment  '
    rezult_string = rezult_string + str(all_closed_deals.filter(status='Закрыта-Рассрочка').count()) + ' / ' \
                    + str(commision)

    if all_closed_deals.filter(status='Срыв').exists():
        commision = (all_closed_deals.filter(status='Срыв').aggregate(commision=Sum('commission', ))['commision'] * \
                 agence_percent) / 100
    else:
        commision = 0
    rezult_string = rezult_string + ' disruption '
    rezult_string = rezult_string + str(all_closed_deals.filter(status='Срыв').count()) + ' / ' + str(commision)

    return rezult_string