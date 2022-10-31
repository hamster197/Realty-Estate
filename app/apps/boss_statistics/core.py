import requests
from django.db.models import Count, Q, Sum
from django.utils import timezone

from app.apps.accounts.models import Departament, MyUser
from app.apps.real_estate.models import CityQuide

contract_types = ['Агентский', 'Эксклюзив']
close_deals_statuses = ['Закрыта', 'Закрыта-Рассрочка']

def get_dates(self):
    if not self.request.GET.get('date_start') or not self.request.GET.get('date_end'):
        date_start = timezone.now().date()
        date_end = timezone.now().date()
    else:
        date_start = self.request.GET.get('date_start')
        date_end = self.request.GET.get('date_end')

    return date_start, date_end

def get_city_queryset(self):
    date_start = get_dates(self)[0]
    date_end = get_dates(self)[1]

    queryset = CityQuide.objects.none()
    if self.request.user.groups.get().name == 'Генеральный директор':
        queryset = CityQuide.objects.all()
    elif self.request.user.groups.get().name == 'Начальник филиала':
        queryset = CityQuide.objects.filter(name=self.request.user.city)

    not_contract_realtys_all = Count('departamint_city_id__user_departamint_id__realty_estate_author_id', distinct=True,
                                     filter=Q(
                                         departamint_city_id__user_departamint_id__realty_estate_author_id__status_obj='Опубликован',
                                         departamint_city_id__user_departamint_id__realty_estate_author_id__contract='Без договора',
                                         departamint_city_id__user_departamint_id__realty_estate_author_id__creation_date__lte=date_end))
    not_contract_realtys_new = Count('departamint_city_id__user_departamint_id__realty_estate_author_id', distinct=True,
                                     filter=Q(
                                         departamint_city_id__user_departamint_id__realty_estate_author_id__status_obj='Опубликован',
                                         departamint_city_id__user_departamint_id__realty_estate_author_id__contract='Без договора',
                                         departamint_city_id__user_departamint_id__realty_estate_author_id__creation_date__gte=date_start))

    contract_realtys_all = Count('departamint_city_id__user_departamint_id__realty_estate_author_id', distinct=True,
                                 filter=Q(
                                     departamint_city_id__user_departamint_id__realty_estate_author_id__status_obj='Опубликован',
                                     departamint_city_id__user_departamint_id__realty_estate_author_id__contract__in=contract_types,
                                     departamint_city_id__user_departamint_id__realty_estate_author_id__creation_date__lte=date_end))
    contract_realtys_new = Count('departamint_city_id__user_departamint_id__realty_estate_author_id', distinct=True,
                                 filter=Q(
                                     departamint_city_id__user_departamint_id__realty_estate_author_id__status_obj='Опубликован',
                                     departamint_city_id__user_departamint_id__realty_estate_author_id__contract__in=contract_types,
                                     departamint_city_id__user_departamint_id__realty_estate_author_id__creation_date__gte=date_start))

    open_deals_sum = Sum('departamint_city_id__user_departamint_id__realtor_in_deal_raltor_id__realtor_commision_sum',
                         distinct=True,
                         filter=Q(
                             departamint_city_id__user_departamint_id__realtor_in_deal_raltor_id__deal__status='Открыта',
                             departamint_city_id__user_departamint_id__realtor_in_deal_raltor_id__deal__date_close_deal__lte=date_end)
                         )
    open_deals_count = Count('departamint_city_id__user_departamint_id__realtor_in_deal_raltor_id', distinct=True,
                             filter=Q(
                                 departamint_city_id__user_departamint_id__realtor_in_deal_raltor_id__deal__status='Открыта',
                                 departamint_city_id__user_departamint_id__realtor_in_deal_raltor_id__deal__date_close_deal__lte=date_end))

    close_deals_sum = Sum('departamint_city_id__user_departamint_id__realtor_in_deal_raltor_id__realtor_commision_sum',
                          distinct=True,
                          filter=Q(
                              departamint_city_id__user_departamint_id__realtor_in_deal_raltor_id__deal__status__in=close_deals_statuses,
                              departamint_city_id__user_departamint_id__realtor_in_deal_raltor_id__deal__date_close_deal__lte=date_end
                          ))
    close_deals_count = Count('departamint_city_id__user_departamint_id__realtor_in_deal_raltor_id', distinct=True,
                              filter=Q(
                                  departamint_city_id__user_departamint_id__realtor_in_deal_raltor_id__deal__status__in=close_deals_statuses,
                                  departamint_city_id__user_departamint_id__realtor_in_deal_raltor_id__deal__date_close_deal__lte=date_end))

    queryset = queryset.annotate(not_contract_realtys_all=not_contract_realtys_all,
                                 not_contract_realtys_new=not_contract_realtys_new,
                                 contract_realtys_all=contract_realtys_all, contract_realtys_new=contract_realtys_new,
                                 open_deals_sum=open_deals_sum, open_deals_count=open_deals_count,
                                 close_deals_sum=close_deals_sum,
                                 close_deals_count=close_deals_count, )
    return queryset

def get_departments_queryset(self):
    
    date_start = get_dates(self)[0]
    date_end = get_dates(self)[1]

    queryset = Departament.objects.none()
    if self.request.user.groups.get().name == 'Генеральный директор':
        queryset = Departament.objects.filter(city__pk=self.kwargs['pk'])
    elif self.request.user.groups.get().name == 'Начальник филиала':
        queryset = Departament.objects.filter(city__pk=self.kwargs['pk'], city=self.request.user.city)

    not_contract_realtys_all = Count('user_departamint_id__realty_estate_author_id', distinct=True,
            filter=Q(
                user_departamint_id__realty_estate_author_id__status_obj='Опубликован',
                user_departamint_id__realty_estate_author_id__contract='Без договора',
                user_departamint_id__realty_estate_author_id__creation_date__lte=date_end))
    not_contract_realtys_new = Count('user_departamint_id__realty_estate_author_id', distinct=True,
            filter=Q(
                user_departamint_id__realty_estate_author_id__status_obj='Опубликован',
                user_departamint_id__realty_estate_author_id__contract='Без договора',
                user_departamint_id__realty_estate_author_id__creation_date__gte=date_start))

    contract_realtys_all = Count('user_departamint_id__realty_estate_author_id', distinct=True,
            filter=Q(
                    user_departamint_id__realty_estate_author_id__status_obj='Опубликован',
                    user_departamint_id__realty_estate_author_id__contract__in=contract_types,
                    user_departamint_id__realty_estate_author_id__creation_date__lte=date_end))
    contract_realtys_new = Count('user_departamint_id__realty_estate_author_id', distinct=True,
            filter=Q(
                    user_departamint_id__realty_estate_author_id__status_obj='Опубликован',
                    user_departamint_id__realty_estate_author_id__contract__in=contract_types,
                    user_departamint_id__realty_estate_author_id__creation_date__gte=date_start))

    open_deals_sum = Sum('user_departamint_id__realtor_in_deal_raltor_id__realtor_commision_sum',
                                 distinct=True,
                                 filter=Q(
                                     user_departamint_id__realtor_in_deal_raltor_id__deal__status='Открыта',
                                     user_departamint_id__realtor_in_deal_raltor_id__deal__date_close_deal__lte=date_end)
                                     )
    open_deals_count = Count('user_departamint_id__realtor_in_deal_raltor_id', distinct=True,
                                 filter=Q(
                                     user_departamint_id__realtor_in_deal_raltor_id__deal__status='Открыта',
                                     user_departamint_id__realtor_in_deal_raltor_id__deal__date_close_deal__lte=date_end))

    close_deals_sum = Sum('user_departamint_id__realtor_in_deal_raltor_id__realtor_commision_sum',
                                  distinct=True,
                                      filter=Q(
                                        user_departamint_id__realtor_in_deal_raltor_id__deal__status__in=close_deals_statuses,
                                        user_departamint_id__realtor_in_deal_raltor_id__deal__date_close_deal__lte=date_end
                                      ))
    close_deals_count = Count('user_departamint_id__realtor_in_deal_raltor_id', distinct=True,
                                 filter=Q(user_departamint_id__realtor_in_deal_raltor_id__deal__status__in=close_deals_statuses,
                                          user_departamint_id__realtor_in_deal_raltor_id__deal__date_close_deal__lte=date_end))

    queryset = queryset.annotate(not_contract_realtys_all=not_contract_realtys_all,
                                 not_contract_realtys_new=not_contract_realtys_new,
                                 contract_realtys_all=contract_realtys_all, contract_realtys_new=contract_realtys_new,
                                 open_deals_sum=open_deals_sum, open_deals_count=open_deals_count,
                                 close_deals_sum=close_deals_sum,
                                 close_deals_count=close_deals_count,
                                 )

    return queryset

def get_realtors_queryset(self):
    date_start = get_dates(self)[0]
    date_end = get_dates(self)[1]
    queryset = MyUser.objects.none()

    if self.action == 'All Realtors':
        queryset = MyUser.objects.filter(is_active=True)
    elif self.request.user.groups.get().name == 'Генеральный директор':
        queryset = MyUser.objects.filter(departament__pk=self.kwargs['pk'], is_active=True)
    elif self.request.user.groups.get().name == 'Начальник филиала':
        queryset = MyUser.objects.filter(departament__pk=self.kwargs['pk'], departament__city=self.request.user.city,
                                         is_active=True)
    elif self.request.user.department_boss:
        queryset = MyUser.objects.filter(departament__pk=self.kwargs['pk'], departament=self.request.user.departament,
                                         is_active=True)


    not_contract_realtys_all = Count('realty_estate_author_id', distinct=True,
            filter=Q(
                realty_estate_author_id__status_obj='Опубликован',
                realty_estate_author_id__contract='Без договора',
                realty_estate_author_id__creation_date__lte=date_end))
    not_contract_realtys_new = Count('realty_estate_author_id', distinct=True,
            filter=Q(
                realty_estate_author_id__status_obj='Опубликован',
                realty_estate_author_id__contract='Без договора',
                realty_estate_author_id__creation_date__gte=date_start))

    contract_realtys_all = Count('realty_estate_author_id', distinct=True,
            filter=Q(
                    realty_estate_author_id__status_obj='Опубликован',
                    realty_estate_author_id__contract__in=contract_types,
                    realty_estate_author_id__creation_date__lte=date_end))
    contract_realtys_new = Count('realty_estate_author_id', distinct=True,
            filter=Q(
                    realty_estate_author_id__status_obj='Опубликован',
                    realty_estate_author_id__contract__in=contract_types,
                    realty_estate_author_id__creation_date__gte=date_start))

    open_deals_sum = Sum('realtor_in_deal_raltor_id__realtor_commision_sum',
                                 distinct=True,
                                 filter=Q(
                                     realtor_in_deal_raltor_id__deal__status='Открыта',
                                     realtor_in_deal_raltor_id__deal__date_close_deal__lte=date_end)
                                     )
    open_deals_count = Count('realtor_in_deal_raltor_id', distinct=True,
                                 filter=Q(
                                     realtor_in_deal_raltor_id__deal__status='Открыта',
                                     realtor_in_deal_raltor_id__deal__date_close_deal__lte=date_end))

    close_deals_sum = Sum('realtor_in_deal_raltor_id__realtor_commision_sum',
                                  distinct=True,
                                      filter=Q(
                                        realtor_in_deal_raltor_id__deal__status__in=close_deals_statuses,
                                        realtor_in_deal_raltor_id__deal__date_close_deal__lte=date_end
                                      ))
    close_deals_count = Count('realtor_in_deal_raltor_id', distinct=True,
                                 filter=Q(realtor_in_deal_raltor_id__deal__status__in=close_deals_statuses,
                                          realtor_in_deal_raltor_id__deal__date_close_deal__lte=date_end))

    queryset = queryset.annotate(not_contract_realtys_all=not_contract_realtys_all,
                                 not_contract_realtys_new=not_contract_realtys_new,
                                 contract_realtys_all=contract_realtys_all, contract_realtys_new=contract_realtys_new,
                                 open_deals_sum=open_deals_sum, open_deals_count=open_deals_count,
                                 close_deals_sum=close_deals_sum,
                                 close_deals_count=close_deals_count,
                                 )

    if self.action == 'All Realtors':
        queryset = queryset.order_by('-close_deals_sum')
    return queryset

def get_user_phone_call(self):
    date_start = get_dates(self)[0]
    date_end = get_dates(self)[1]
    user = self.object

    url = "https://cloudpbx.beeline.ru/apis/portal/records?userId=" + str(user.phone) + "%40ip.beeline.ru" + \
          '&dateFrom=' + str(date_start) + 'T00%3A00%3A00.000Z&dateTo=' + str(date_end) + 'T23%3A00%3A00.000Z'
    payload = {}
    from sait_settings import BEELINE_TOKEN, BEELINE_COOKIE
    headers = {
        'X-MPBX-API-AUTH-TOKEN': BEELINE_TOKEN,
        'Cookie': BEELINE_COOKIE
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    calls_counter = 0
    for i in response.json():
        calls_counter += 1
    import numpy as np
    calls_array = np.chararray((calls_counter, 3), itemsize=185, unicode=True)
    calls_counter = 0
    if response.text == '{"errorCode":"UserNotFound","description":"Для заданного идентификатора нет абонента"}':
        calls_array[0][0] = 'Для заданного идентификатора нет абонента'
    else:
        for i in response.json():
            call_id = str(i['id'])
            url = "https://cloudpbx.beeline.ru/apis/portal/records/" + call_id + "/reference"

            payload = {}
            headers = {
                'X-MPBX-API-AUTH-TOKEN': 'db73cb07-1624-45ab-8ea2-4decea1db7a0',
                'Cookie': 'SRVNAME=AAP'
            }

            response_call = requests.request("GET", url, headers=headers, data=payload)
            calls_array[calls_counter][0] = str(i['phone'])
            calls_array[calls_counter][1] = round(i['duration'] / 60000, 2)  # /60/60
            calls_array[calls_counter][2] = response_call.json()['url']
            calls_counter += 1

    return calls_array