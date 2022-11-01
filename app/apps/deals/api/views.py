from rest_framework.generics import ListAPIView, ListCreateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from rest_framework.viewsets import ModelViewSet

from app.apps.deals.api.filters import RealtorInTheDealFilter, SubmittedCommissionFilter
from app.apps.deals.api.mixins import IsBoss
from app.apps.deals.api.serializers import *
from app.apps.deals.core import OpenDealList


class SalesChanelsViewSet(ListAPIView):
    """
           Перечисляет открытые сделки(Открыта, Рассрочка).
           permission_classes = (IsAuthenticated,)
    """
    queryset = SalesChanelQuide.objects.all()
    serializer_class = SalesChanelQuideSerializer
    permission_classes = (IsAuthenticated,)

class DealsOpenViewSet(ListCreateAPIView):
    """
           Перечисляет открытые сделки('Открыта', 'Рассрочка').
           permission_classes = (IsAuthenticated,)
    """
    serializer_class = DealSerializer
    permission_classes = (IsAuthenticated,)
    deal_status = ''

    def get_queryset(self):
        deal_status = []
        deal_status.append(self.deal_status)
        return OpenDealList(self.request.user, deal_status)

    def perform_create(self, serializer):

        if self.deal_status == 'Открыта':
            instancse = serializer.save(status=self.deal_status, )
            RealtorInTheDeal.objects.create(deal=instancse, name=self.request.user, percent=10)

        elif self.deal_status == 'Рассрочка':
            instancse = serializer.save(status=self.deal_status, )
            RealtorInTheDeal.objects.create(deal=instancse, name=self.request.user, percent=10)

class DealsCloseViewSet(ListAPIView):
    """
           Перечисляет закрытые сделки('Закрыта-Рассрочка', 'Закрыта', 'Срыв',).
           permission_classes = (IsAuthenticated,)
    """
    serializer_class = DealSerializer
    filterset_class = ''
    permission_classes = (IsAuthenticated,)
    deal_status = ''

    def get_queryset(self):
        start_date = timezone.now().replace(hour=0, minute=0, second=0, day=1)
        end_date = timezone.now().replace(hour=23, minute=59, second=59)
        deal_status = []
        deal_status.append(self.deal_status)
        return OpenDealList(self.request.user, deal_status)\
            .filter(date_close_deal__gte=start_date, date_close_deal__lte=end_date)

class DealsUpdateViewSet(UpdateAPIView):
    """
           Обновляет сделки('Открыта','Рассрочка',).
           permission_classes = (IsAuthenticated, IsBoss)
    """
    queryset = Deal.objects.all()
    serializer_class = DealIsBossSerializer
    permission_classes = (IsAuthenticated, IsBoss)

    def get_queryset(self):
        deal_status = ['Открыта','Рассрочка',]
        return OpenDealList(self.request.user, deal_status)

class DealsRealtorViewSet(ModelViewSet):
    """
           Перечисляет, создает и редактирует риелторов и их проценты в сделке.
           Фильтрует по pk сделки
           permission_classes = (IsAuthenticated, IsBoss)
    """
    queryset = RealtorInTheDeal.objects.all()
    serializer_class = DealRealtorsSerializer
    permission_classes = (IsAuthenticated, IsBoss)
    filterset_class = RealtorInTheDealFilter

class SubmittedCommissionViewSet(ModelViewSet):
    """
           Перечисляет, создает и коммисии в сделке.
           Фильтрует по pk коммисии
           permission_classes = (IsAuthenticated, IsBoss)
    """
    queryset = SubmittedCommission.objects.all()
    serializer_class = SubmittedCommissionSerializer
    permission_classes = (IsAuthenticated, IsBoss)
    filterset_class = SubmittedCommissionFilter






