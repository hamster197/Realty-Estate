
from django.urls import path, include

from app.apps.deals.filters import *
from app.apps.deals.views import *

app_name = 'deal_urls'

urlpatterns = [
    path('open/', DealsOpenList.as_view(deal_status='Открыта'), name='deal_open_url'),
    path('installment/', DealsOpenList.as_view(deal_status='Рассрочка'), name='deal_installment_url'),
    path('closed/', DealsNotOpenList.as_view(filterset_class=DealClosedFilter), name='deal_closed_url'),
    path('closed_installment/', DealsNotOpenList.as_view(filterset_class=DealInstallmentClosedFilter),
         name='deal_closed_installment_url'),
    path('disruption/', DealsNotOpenList.as_view(filterset_class=DealDisruptionFilter), name='deal_disruption_url'),
    path('detail/<int:pk>/', DealDetail.as_view(), name='deal_detail_url'),

    path('new/', DealNew.as_view(), name='deal_new_url'),
    path('edit/<pk>/', DealEdit.as_view(), name='deal_edit_url'),

    path('reiting/', DealReiting.as_view(filterset_class=DealReitingFilterMixin), name='deal_reiting_url'),
    path('reiting/department/', DealReiting.as_view(filterset_class=DealDepartmentReitingFilter),
         name='deal_department_reiting_url'),
    path('reiting/city/', DealReiting.as_view(filterset_class=DealCityReitingFilter),
         name='deal_city_reiting_url'),

    path('api/v1/', include('app.apps.deals.api.urls'), )
]
