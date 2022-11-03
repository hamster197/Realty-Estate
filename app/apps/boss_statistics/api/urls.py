from django.urls import re_path, path, register_converter
from datetime import date, datetime

from app.apps.boss_statistics.api.views import *


class DateConverter:
    regex = r"\d{4}-\d{1,2}-\d{1,2}"
    format = "%Y-%m-%d"

    def to_python(self, value: str) -> date:
        return datetime.strptime(value, self.format).date()

    def to_url(self, value: date) -> str:
        return value.strftime(self.format)


register_converter(DateConverter, "date")

urlpatterns = [
    re_path('sity_list/(?P<date_start>.+)/(?P<date_end>.+)/', InstatnseStatisticViewSet.as_view(action='Cityes'),
            name='sity_list_url'),
    re_path('departments_list/(?P<date_start>.+)/(?P<date_end>.+)/(?P<pk>.+)/',
            InstatnseStatisticViewSet.as_view(action='Departments'),  name='departments_list_url'),
    re_path('realtors_list/(?P<date_start>.+)/(?P<date_end>.+)/(?P<pk>.+)/',
            InstatnseStatisticViewSet.as_view(action='Realtors'), name='realtors_list_list_url'),
    re_path('realtors_list_all/(?P<date_start>.+)/(?P<date_end>.+)/',
            InstatnseStatisticViewSet.as_view(action='All Realtors'), name='realtors_list_all_list_url'),

    path('realtor_estates/<int:pk>/', RealtyEstateViewSet.as_view(action='Estates'),
            name='realtor_estates_url'),
    path('client_estates/<int:pk>/', RealtyEstateViewSet.as_view(action='Clients'),
            name='client_estates_url'),
    path('phone_calls/<int:pk>/<date:date_start>/<date:date_end>/', PhoneCallsViewSet.as_view(), name='phone_calls_url'),

]

