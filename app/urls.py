
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

handler404 = 'app.views.v404_view'
handler500 = 'app.views.v404_view'

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
    path('boss_statistics/', include('app.apps.boss_statistics.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
