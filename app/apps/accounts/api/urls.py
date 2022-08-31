from django.urls import path, include, re_path

from app.apps.accounts.api.views import DepartamentQuideViewSet

urlpatterns = [
    path('auth/', include('djoser.urls')),
    re_path('auth/', include('djoser.urls.authtoken')),
    path('v1/department_list/', DepartamentQuideViewSet.as_view(), name='department_list')
]

