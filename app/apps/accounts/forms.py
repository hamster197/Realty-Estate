from django.contrib.auth.forms import AuthenticationForm

from app.apps.accounts.models import MyUser


class LoginForm(AuthenticationForm):
    class Meta:
        model = MyUser
        exclude = []