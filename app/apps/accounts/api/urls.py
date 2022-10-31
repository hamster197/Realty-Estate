from django.urls import path, include, re_path
from rest_framework import routers

from app.apps.accounts.api.views import *

router = routers.SimpleRouter()

router.register('city_admin', SityQuideViewSet, basename='city_admin_url')
router.register('department_admin', DepartamentQuideViewSet, basename='department_admin_url')
router.register('district_admin', DistrictQuideViewSet, basename='district_admin_url')
router.register('sales_chanel_admin', SalesChanelQuideViewSet, basename='sales_chanel_admin_url')

urlpatterns = [
    path('auth/', include('djoser.urls')),
    re_path('auth/', include('djoser.urls.authtoken')),

    path('sity_list/', SityQuideList.as_view(), name='sity_list_url'),
    path('department_list/', DepartamentQuideList.as_view(), name='department_list_url'),
    path('district_list/', DistrictQuideList.as_view(), name='district_list_url'),

    path('groups_list/', GroupQuideViewSet.as_view(), name='groups_list_url'),

    # path('estates_trasfer/', UserSubjectTransfer.as_view(action='estates trasfer'), name='estates_trasfer_url'),
    # path('clients_trasfer/', UserSubjectTransfer.as_view(action='clients trasfer'), name='clients_trasfer_url'),
    path('trasfer/<action>/', UserSubjectTransfer.as_view(), name='estates_trasfer_url'),

]

urlpatterns += router.urls