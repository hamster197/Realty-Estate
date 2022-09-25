from django.urls import path
from rest_framework import routers

from app.apps.real_estate.api.views import MyFlateViewSet, MyHouseViewSet, MyPlotOfLandsViewSet, MyCommerceViewSet, \
    RealtyEstateGaleryViewSet, DistrictQuideViewSet, CityQuideViewSet, MyClientViewSet, AllClientViewSet, \
    AvailableEstatesForClientViewSet, AvailableClientsForEstatesViewSet

router = routers.SimpleRouter()

router.register('my_flats', MyFlateViewSet, basename='my_flats_url')
router.register('my_houses', MyHouseViewSet, basename='my_houses_url')
router.register('my_plot_of_lands', MyPlotOfLandsViewSet, basename='my_plot_of_lands_url')
router.register('my_comerce', MyCommerceViewSet, basename='my_houses')

router.register('estate_galery', RealtyEstateGaleryViewSet, basename='estate_galery_url')

router.register('clients_my', MyClientViewSet, basename='clients_my_url')
router.register('clients_all', AllClientViewSet, basename='clients_all_url')

urlpatterns = [
    path('quide_sitys/', CityQuideViewSet.as_view(), name='quide_sitys_url'),
    path('quide_districts/', DistrictQuideViewSet.as_view(), name='quide_districts_url'),

    path('available_estates_for_client/<int:pk>/', AvailableEstatesForClientViewSet.as_view(),
         name='available_estates_for_client_url'),
    path('available_client_for_estates/<int:pk>/', AvailableClientsForEstatesViewSet.as_view(),
         name='available_client_for_estates_url'),
]
urlpatterns += router.urls