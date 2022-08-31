from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from app.apps.real_estate.api.filters import DrfMyFlatRealtyEstateFilter, DrfMyHouseRealtyEstateFilter, \
    DrfMyPlotOfLandRealtyEstateFilter, DrfMyCommerceRealtyEstateFilter, MyClientFilter, AllClientFilter
from app.apps.real_estate.api.serializers import MyFlatsSerializer, MyHousesSerializer, MyPlotOfLandsSerializer, \
    MyCommercesSerializer, RealtyEstateGalerySerializer, DistrictQuideSerializer, CityQuideSerializer, \
    AllRealtySerializer, MyClientSerializer, AllClientSerializer, RealtySerializer
from app.apps.real_estate.models import Flat, House, PlotOfLand, Commerce, RealtyEstateGalery, DistrictQuide, CityQuide, \
    RealtyEstate, Client


class CityQuideViewSet(ListAPIView):
    """
           Перечисляет города .
           permission_classes = (IsAuthenticated,)
    """
    queryset = CityQuide.objects.all()
    serializer_class = CityQuideSerializer
    permission_classes = (IsAuthenticated,)

class DistrictQuideViewSet(ListAPIView):
    """
           Перечисляет районы с привязкой к городам.
           permission_classes = (IsAuthenticated,)
    """
    queryset = DistrictQuide.objects.all()
    serializer_class = DistrictQuideSerializer
    permission_classes = (IsAuthenticated,)

class AllRealtyEstateViewSet(ListAPIView):
    """
           Перечисляет все обьекты(за исключением обьектов пользователя).
           permission_classes = (IsAuthenticated,)
    """
    serializer_class = AllRealtySerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return RealtyEstate.objects.filter()


class RealtyEstateViewSet(ModelViewSet):

    permission_classes = (IsAuthenticated, )
    http_method_names = ['get', 'post', 'put', 'patch', 'head', 'options', 'trace']

    def get_queryset(self):
        if self.serializer_class == MyFlatsSerializer:
            return Flat.objects.filter(author=self.request.user, status_obj='Опубликован')
        elif self.serializer_class == MyHousesSerializer:
            return House.objects.filter(author=self.request.user, status_obj='Опубликован')
        elif self.serializer_class == MyPlotOfLandsSerializer:
            return PlotOfLand.objects.filter(author=self.request.user, status_obj='Опубликован')
        elif self.serializer_class == MyCommercesSerializer:
            return Commerce.objects.filter(author=self.request.user)

    def perform_create(self, serializer):
        if self.serializer_class == MyFlatsSerializer:
            serializer.save(type='Квартира', author=self.request.user,)
        elif self.serializer_class == MyHousesSerializer:
            serializer.save(type='Дом', author=self.request.user,)
        elif self.serializer_class == MyPlotOfLandsSerializer:
            serializer.save(type='Участок', author=self.request.user,)
        elif self.serializer_class == MyCommercesSerializer:
            serializer.save(type='Коммерция', author=self.request.user,)

class MyFlateViewSet(RealtyEstateViewSet):
    """
           Перечисляет активныеквартиры пользователя или создает и редактирует квартиру.
           permission_classes = (IsAuthenticated,)
    """
    serializer_class = MyFlatsSerializer
    filterset_class = DrfMyFlatRealtyEstateFilter

class MyHouseViewSet(RealtyEstateViewSet):
    """
           Перечисляет активные дома пользователя или создает и редактирует дом.
           permission_classes = (IsAuthenticated,)
    """
    serializer_class = MyHousesSerializer
    filterset_class = DrfMyHouseRealtyEstateFilter

class MyPlotOfLandsViewSet(RealtyEstateViewSet):
    """
           Перечисляет активные участки пользователя или создает и редактирует участок.
           permission_classes = (IsAuthenticated,)
    """
    serializer_class = MyPlotOfLandsSerializer
    filterset_class = DrfMyPlotOfLandRealtyEstateFilter

class MyCommerceViewSet(RealtyEstateViewSet):
    """
           Перечисляет активную коммерцию пользователя или создает и редактирует коммерцию.
           permission_classes = (IsAuthenticated,)
    """
    serializer_class = MyCommercesSerializer
    filterset_class = DrfMyCommerceRealtyEstateFilter

class RealtyEstateGaleryViewSet(ModelViewSet):
    """
           Перечисляет галерею картинок обьекта недвижимости пользователя.
           permission_classes = (IsAuthenticated,)
    """

    permission_classes = (IsAuthenticated, )
    http_method_names = ['get', 'post', 'put', 'patch', 'head', 'options', 'trace', 'delete',]
    serializer_class = RealtyEstateGalerySerializer

    def get_queryset(self):
        return RealtyEstateGalery.objects.filter(realty_estate__author=self.request.user)

class AvailableClientsForEstatesViewSet(ListAPIView):
    """
           фильтрует доступныкллиентов по цене и району. Принимает pk обьекта надвижимости .
           permission_classes = (IsAuthenticated,)
    """
    serializer_class = MyClientSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        estate = get_object_or_404(RealtyEstate, pk=self.kwargs['pk'])
        return Client.objects.filter(estate_type=estate.type,
            district=estate.district, status=False,
            min_price__lte=estate.agency_price, max_price__gte=estate.agency_price)

class MyClientViewSet(ModelViewSet):
    """
           Перечисляет активных клиентов пользователя.
           permission_classes = (IsAuthenticated,)
    """

    permission_classes = (IsAuthenticated, )
    http_method_names = ['get', 'post', 'put', 'patch', 'head', 'options', 'trace', 'delete',]
    serializer_class = MyClientSerializer
    filterset_class = MyClientFilter

    def get_queryset(self):
        return Client.objects.filter(author=self.request.user, status=False)

class AllClientViewSet(MyClientViewSet):
    """
           Перечисляет активных клиентов.
           permission_classes = (IsAuthenticated,)
    """
    serializer_class = AllClientSerializer
    filterset_class = AllClientFilter
    def get_queryset(self):
        return Client.objects.filter(status=False).exclude(author=self.request.user,)

class AvailableEstatesForClientViewSet(ListAPIView):
    """
           фильтрует доступные обьекты недвижимости по цене и району. Принимает pk клиента .
           permission_classes = (IsAuthenticated,)
    """
    serializer_class = RealtySerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        client = get_object_or_404(Client, pk=self.kwargs['pk'])
        return RealtyEstate.objects.filter(type=client.estate_type,
            district__in=client.district.all(), status_obj='Опубликован',
            agency_price__gt=client.min_price, agency_price__lte=client.max_price)








