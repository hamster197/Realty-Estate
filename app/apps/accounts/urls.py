from django.contrib.auth.views import LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordChangeView
from django.urls import path, reverse_lazy

from app.apps.accounts.views import FirstPage

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
]
