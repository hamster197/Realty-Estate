from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
from django.views.generic import ListView, DetailView
from datetime import datetime
from app.apps.accounts.models import MyUser
from app.apps.boss_statistics.core import get_city_queryset, get_departments_queryset, get_realtors_queryset, \
    get_user_phone_call
from app.apps.real_estate.models import RealtyEstate, Client


class InstanseBossStat(LoginRequiredMixin, ListView):
    template_name = 'boss_statistics/instanses_list.html'
    context_object_name = 'instanses'
    action = ''

    def get_queryset(self):
        # if 'Realtors' in self.action:
        #     print('1')
        if self.action == 'Cityes':
            return get_city_queryset(self)
        if self.action == 'Departments':
            return get_departments_queryset(self)
        if 'Realtors' in self.action:
            return get_realtors_queryset(self)

class UserDetailBossStat(LoginRequiredMixin, DetailView):
    template_name = 'boss_statistics/user_detail.html'
    context_object_name = 'instanse'
    action = ''

    def get_queryset(self):
        queryset = None
        if self.request.user.groups.get().name == 'Генеральный директор':
            queryset = MyUser.objects.filter(is_active=True)
        elif self.request.user.groups.get().name == 'Начальник филиала':
            queryset = MyUser.objects.filter(departament__city=self.request.user.city,
                                             is_active=True)
        elif self.request.user.department_boss:
            queryset = MyUser.objects.filter(departament=self.request.user.departament,
                                             is_active=True)
        return queryset

    def get_context_data(self, **kwargs):

        context = super(UserDetailBossStat, self).get_context_data(**kwargs)
        if self.action == 'Estates':
            context['context'] = RealtyEstate.objects.filter(author=self.object)
        if self.action == 'Clients':
            context['context'] = Client.objects.filter(author=self.object, status=False)
        if self.action == 'Calls':
            context['calls_array'] = get_user_phone_call(self)

        return context
