"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path

from app import settings

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Small RealtyEstate CRM API",
      default_version='v1',
      description="Small RealtyEstate CRM.",
      terms_of_service="No terms",
      contact=openapi.Contact(email="contact@mail.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.IsAdminUser,),
)

urlpatterns = [
    re_path('swagger(\.json|\.yaml)', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0, ), name='schema-swagger-ui',
         ),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('select2/', include("django_select2.urls")),

    path('admin/', admin.site.urls),

    path('', include('app.apps.accounts.urls')),
    path('real_estates/', include('app.apps.real_estate.urls')),
    path('deals/', include('app.apps.deals.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
