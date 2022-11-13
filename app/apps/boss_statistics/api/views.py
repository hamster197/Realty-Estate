from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from app.apps.accounts.models import MyUser
from app.apps.boss_statistics.api.serializers import *
from app.apps.boss_statistics.core import get_city_queryset, get_departments_queryset, get_realtors_queryset, \
    get_user_phone_call
from app.apps.real_estate.models import RealtyEstate, Client


class InstatnseStatisticViewSet(generics.ListAPIView):
    """
        Отображает статистику по обьектам с договорами(contract_realtys_all(все) contract_realtys_new(за месяц))
        без договoров (not_contract_realtys_all(все) not_contract_realtys_new(за месяц))
        обшей суммы по откр сделкам(open_deals_sum) их кол-во (open_deals_count)
        обшей суммы по закр сделкам(close_deals_sum) их кол-во (close_deals_count)
    """
    permission_classes = (IsAuthenticated,)
    action = ''
    swagger_schema = None

    def get_queryset(self):
        if self.action == 'Cityes':
            return get_city_queryset(self)
        if self.action == 'Departments':
            return get_departments_queryset(self)
        if 'Realtors' in self.action:
            return get_realtors_queryset(self)

    def get_serializer_class(self):
        if self.action == 'All Realtors':
            return InstatnseReitingSerializer
        return InstatnseStatisticSerializer


def check_user_account_right(self, agent):
    if self.request.user.groups.get().name == 'Генеральный директор':
        return True

    if self.request.user.groups.get().name == 'Начальник филиала':
        if agent.departament:
            if self.request.user.city == agent.departament.city:
                return True

    if self.request.user.department_boss:
        if self.request.user.departament == agent.departament:
            return True

    return False

class RealtyEstateViewSet(ListAPIView):
    """
           Перечисляет активных обьекты пользователя.
           permission_classes = (IsAuthenticated,)
    """

    permission_classes = (IsAuthenticated, )
    action = ''
    swagger_schema = None

    def get_queryset(self):
        queryset = RealtyEstate.objects.none()
        agent = get_object_or_404(MyUser, pk=self.kwargs['pk'])
        if check_user_account_right(self, agent)==True:
            if self.action == 'Estates':
                queryset = RealtyEstate.objects.filter(author=agent, status_obj='Опубликован')
            elif self.action == 'Clients':
                queryset = Client.objects.filter(author=agent, status=False)

        return queryset

    def get_serializer_class(self):
        if self.action == 'Estates':
            return RealtyEstateSerializer
        if self.action == 'Clients':
            return ClientSerializer


class PhoneCallsViewSet(APIView):
    """
           Перечисляет Звонки пользователя.
           permission_classes = (IsAuthenticated,)
    """
    object = None

    def get(self, request, **kwargs):
        agent =self.object = get_object_or_404(MyUser, pk=self.kwargs['pk'])
        if check_user_account_right(self, agent)==True:
            return Response({'phone calls': get_user_phone_call(self, agent.pk)})
        else:
            return Response({'phone calls': None })

