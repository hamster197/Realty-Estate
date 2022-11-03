from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from app.apps.accounts.api.serializers import *
from app.apps.accounts.models import Departament
from app.apps.deals.api.serializers import SalesChanelQuideSerializer
from app.apps.deals.models import SalesChanelQuide
from app.apps.real_estate.models import CityQuide, RealtyEstate, Client


class GroupQuideViewSet(ListAPIView):
    """
           Перечисляет группы(Риелтор, Начальник филиала, Генеральный директор).
           permission_classes = (IsAdminUser,)
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (IsAdminUser, )

class SityQuideList(ListAPIView):
    """
           Перечисляетгорода в справочник.
           permission_classes = (IsBoss)
    """
    queryset = CityQuide.objects.all()
    serializer_class = CitySerializer
    permission_classes = (IsAuthenticated, )

class SityQuideViewSet(ModelViewSet):
    """
           Перечисляет, создает и редактирует города в справочник.
           permission_classes = (IsBoss)
    """
    queryset = CityQuide.objects.all()
    serializer_class = CitySerializer
    permission_classes = (IsAdminUser, )

class DepartamentQuideList(ListAPIView):
    """
           Перечисляет Отделы.
           permission_classes = (IsAuthenticated,)
    """
    queryset = Departament.objects.all()
    serializer_class = DepartamentSerializer
    permission_classes = (IsAuthenticated, )

class DepartamentQuideViewSet(ModelViewSet):
    """
           Перечисляет, создает и редактирует города в справочник.
           permission_classes = (IsBoss)
    """
    queryset = Departament.objects.all()
    serializer_class = DepartamentSerializer
    permission_classes = (IsAdminUser, )

class DistrictQuideList(ListAPIView):
    """
           Перечисляет Районы.
           permission_classes = (IsAuthenticated,)
    """
    queryset = DistrictQuide.objects.all()
    serializer_class = DistrictSerializer
    permission_classes = (IsAuthenticated, )

class DistrictQuideViewSet(ModelViewSet):
    """
           Перечисляет, создает и редактирует города в справочник.
           permission_classes = (IsBoss)
    """
    queryset = DistrictQuide.objects.all()
    serializer_class = DistrictSerializer
    permission_classes = (IsAdminUser, )

class SalesChanelQuideViewSet(ModelViewSet):
    """
           Перечисляет, создает и редактирует Каналы продаж в справочник.
           permission_classes = (IsBoss)
    """
    queryset = SalesChanelQuide.objects.all()
    serializer_class = SalesChanelQuideSerializer
    permission_classes = (IsAdminUser, )

class UserSubjectTransfer(APIView):
    """
           переносит клиентов(trasfer/clients)/обьекты(/trasfer/estates)/недвижимость между пользователями
           permission_classes = (IsAdminUser, ),
    """
    serializer_class = SubjectTransferSerializer
    permission_classes = (IsAdminUser,)
    http_method_names = ['post', ]

    def post(self, request, **kwargs):
        serializer = SubjectTransferSerializer(data=request.data)
        counter = ''
        error = ''
        if serializer.is_valid():
            user_from = get_object_or_404(MyUser, pk=serializer.data['user_from'])
            user_to = get_object_or_404(MyUser, pk=serializer.data['user_to'])
            if self.kwargs['action'] == 'estates':
                subj = RealtyEstate.objects.filter(author=user_from)
                counter = str(subj.count())
                subj.update(author=user_to)
            if self.kwargs['action'] == 'clients':
                subj = Client.objects.filter(author=user_from)
                counter = str(subj.count())
                subj.update(author=user_to)
        else:
            error = serializer.errors['non_field_errors'][0]
        return Response(counter + ' ' + self.kwargs['action'] + error)
