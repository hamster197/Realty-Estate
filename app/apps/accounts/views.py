from django.contrib.auth.views import LoginView
from django.shortcuts import redirect


# Create your views here.


class FirstPage(LoginView):
    from app.apps.accounts.forms import LoginForm
    template_name = 'accounts/first_page.html'
    authentication_form = LoginForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('real_estates_urls:all_real_estates_url')
        return super().dispatch(request, *args, **kwargs)

