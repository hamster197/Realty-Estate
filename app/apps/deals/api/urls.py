from django.urls import path
from rest_framework import routers

from app.apps.deals.api.views import *
from app.apps.deals.filters import DealClosedFilter

router = routers.SimpleRouter()

router.register('realtors_in_deal', DealsRealtorViewSet, basename='realtors_in_deal_url')

router.register('submitted_commission_of_deal', SubmittedCommissionViewSet, basename='submitted_commission_of_deal_url')


urlpatterns = [
    path('sales_chanels_list/', SalesChanelsViewSet.as_view(), name='sales_chanels_list_url'),

    path('open_deals/', DealsOpenViewSet.as_view(deal_status='Открыта'), name='open_deals_list_url'),
    path('installment/', DealsOpenViewSet.as_view(deal_status='Рассрочка'), name='installment_deals_list_url'),
    path('closed/', DealsCloseViewSet.as_view(filterset_class=DealClosedFilter, deal_status='Закрыта'),
         name='closed_deals_list_url'),
    path('closed_installment/', DealsCloseViewSet.as_view(deal_status='Закрыта-Рассрочка'),
         name='closed_installment_deals_list_url'),
    path('disruption/', DealsCloseViewSet.as_view(deal_status='Срыв'), name='disruption_deals_list_url'),

    path('edit/<int:pk>/', DealsUpdateViewSet.as_view(), name='edit_deals_url'),

]

urlpatterns += router.urls