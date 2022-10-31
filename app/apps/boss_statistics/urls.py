
from django.urls import path

from app.apps.boss_statistics.views import *

app_name = 'boss_statistics_urls'

urlpatterns = [
    path('cityes_list/', InstanseBossStat.as_view(action='Cityes', ), name='sityes_list_url'),
    path('departments_list_test/<int:pk>/', InstanseBossStat.as_view(action='Departments', ), name='departments_list_url'),
    path('realtors_list/<int:pk>/', InstanseBossStat.as_view(action='Realtors', ), name='realtors_list_url'),
    path('realtors_list_all/', InstanseBossStat.as_view(action='All Realtors', ), name='realtors_list_all'),

    path('realtor_detail/<int:pk>/', UserDetailBossStat.as_view(action='Estates',), name='realtor_detail_url'),
    path('realtor_detail_clients/<int:pk>/', UserDetailBossStat.as_view(action='Clients',), name='realtor_clients_url'),
    path('realtor_detail_calls/<int:pk>/', UserDetailBossStat.as_view(action='Calls',), name='realtor_detail_calls'),

    #path('api/v1/', include('app.apps.accounts.api.urls'),)
]
