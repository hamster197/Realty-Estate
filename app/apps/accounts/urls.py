from django.contrib.auth.views import LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordChangeView
from django.urls import path, include

#from app.apps.accounts.models import Departament
from app.apps.accounts.models import Departament
from app.apps.accounts.views import *
from app.apps.deals.models import SalesChanelQuide
from app.apps.real_estate.models import DistrictQuide, CityQuide

app_name = 'accounts_urls'

urlpatterns = [
    path('', FirstPage.as_view(), name='first_page_url'),
    path('logout/', LogoutView.as_view(), name='logout_url'),

    path('password_change/', PasswordChangeView.as_view(template_name='accounts/password_change_form.html',
                                                       success_url=reverse_lazy('accounts_urls:reset_password_done')),
         name='password_change_url'),

    path('password_reset_start/', PasswordResetView.as_view(template_name='accounts/password_reset_form.html',
                                                       email_template_name='accounts/password_reset_email.html',
                                                       success_url=reverse_lazy('accounts_urls:reset_password_done')),
         name='reset_password_url'),
    path('password_reset/done/', PasswordResetDoneView.as_view(template_name = 'accounts/password_reset_done_form.html'),
         name='reset_password_done'),
    path('password_reset_confirm/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confim_form.html', ),
         name='password_reset_confirm'),

    path('users/list/', UsersList.as_view(), name='users_list_url'),
    path('users/edit/<int:pk>/', UserUpdate.as_view(), name='users_edit_url'),
    path('users/new/', UserCreate.as_view(), name='users_new_url'),
    path('users/transfer/', AdminSubjectTransfer.as_view(), name='users_subject_transfer_url'),

    path('sitys_quide/', QuidesEdit.as_view(model=CityQuide, action='City quide',
                                  success_url=reverse_lazy('accounts_urls:sitys_quide_url')), name='sitys_quide_url'),
    path('departments_quide/', QuidesEdit.as_view(model=Departament, action='Departments quide',
                               success_url=reverse_lazy('accounts_urls:departments_quide_url')),
         name='departments_quide_url'),
    path('district_quide/', QuidesEdit.as_view(model=DistrictQuide, action='District quide',
                               success_url=reverse_lazy('accounts_urls:district_quide_url')), name='district_quide_url'),
    path('sales_chanels_quide/', QuidesEdit.as_view(model=SalesChanelQuide, action='Sales Chanels quide',
                               success_url=reverse_lazy('accounts_urls:sales_chanels_quide_url')),

         name='sales_chanels_quide_url'),

    path('api/v1/', include('app.apps.accounts.api.urls'),)
]
