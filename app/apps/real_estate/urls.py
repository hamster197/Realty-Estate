
from django.urls import path

from app.apps.real_estate.filters import MyFlatRealtyEstateFilter, MyCommerceRealtyEstateFilter, \
    MyPlotOfLandRealtyEstateFilter, MyHouseRealtyEstateFilter
from app.apps.real_estate.forms import CommerceEditForm, FlatEditForm, HouseEditForm, PlotOfLandEditForm
from app.apps.real_estate.models import Flat, House, PlotOfLand, Commerce
from app.apps.real_estate.views import AllRealEstates, InstanceNew, InstanceEdit, MyRealtyDetail, \
    MyRealtyEstates, YandexFeed

app_name = 'real_estates_urls'

urlpatterns = [
    path('', AllRealEstates.as_view(), name='all_real_estates_url'),
    path('my/flat/', MyRealtyEstates.as_view(filterset_class=MyFlatRealtyEstateFilter), name='my_flat_list_url'),
    path('my/house/', MyRealtyEstates.as_view(filterset_class=MyHouseRealtyEstateFilter), name='my_house_list_url'),
    path('my/plot_of_land/', MyRealtyEstates.as_view(filterset_class=MyPlotOfLandRealtyEstateFilter), name='my_plot_of_landt_list_url'),
    path('my/commerce/', MyRealtyEstates.as_view(filterset_class=MyCommerceRealtyEstateFilter), name='my_commerce_list_url'),

    path('flat/detail/<int:pk>/', MyRealtyDetail.as_view(model=Flat), name='flat_detail_url'),
    path('house/detail/<int:pk>/', MyRealtyDetail.as_view(model=House), name='house_detail_url'),
    path('plot_of_land/detail/<int:pk>/', MyRealtyDetail.as_view(model=PlotOfLand), name='plot_of_land_detail_url'),
    path('commerce/detail/<int:pk>/', MyRealtyDetail.as_view(model=Commerce), name='commerce_detail_url'),

    path('flat/new/', InstanceNew.as_view(form_class=FlatEditForm), name='new_flat_url'),
    path('house/new/', InstanceNew.as_view(form_class=HouseEditForm), name='new_house_url'),
    path('plot_of_land/new/', InstanceNew.as_view(form_class=PlotOfLandEditForm), name='new_plot_of_land_url'),
    path('commerce/new/', InstanceNew.as_view(form_class=CommerceEditForm,), name='new_commerce_url'),

    path('flat/edit/<int:pk>/', InstanceEdit.as_view(form_class=FlatEditForm), name='edit_flat_url'),
    path('house/edit/<int:pk>/', InstanceEdit.as_view(form_class=HouseEditForm), name='edit_house_url'),
    path('plot_of_land/edit/<int:pk>/', InstanceEdit.as_view(form_class=PlotOfLandEditForm),
         name='edit_plot_of_land_url'),
    path('commerce/edit/<int:pk>/', InstanceEdit.as_view(form_class=CommerceEditForm), name='edit_commerce_url'),

    path('yandex.xml', YandexFeed.as_view(), name='yandex_url'),
]
