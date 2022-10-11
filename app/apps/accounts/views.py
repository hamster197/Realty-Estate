from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib import messages
# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import UpdateView, CreateView, TemplateView

from django_filters.views import FilterView
from extra_views import ModelFormSetView

from app.apps.accounts.filters import UserListFilter
from app.apps.accounts.forms import *
from app.apps.deals.models import SalesChanelQuide
from app.apps.real_estate.models import RealtyEstate, Client, CityQuide


class FirstPage(LoginView):
    template_name = 'accounts/first_page.html'
    authentication_form = LoginForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('real_estates_urls:all_real_estates_url')
        return super().dispatch(request, *args, **kwargs)

class UsersList(PermissionRequiredMixin, FilterView):
    permission_required = 'is_staff'
    template_name = 'accounts/users_list.html'
    context_object_name = 'instances'
    filterset_class = UserListFilter

class UserUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'is_staff'
    template_name = 'accounts/user_edit.html'
    form_class = UserEditForm
    model = MyUser

    def get_context_data(self, **kwargs):
        context = super(UserUpdate, self).get_context_data(**kwargs)
        context['password_form'] = PswChangeForm(self.get_object())
        context['action'] = 'edit'
        return context

    def post(self, request, *args, **kwargs):
        if '_change_password' in request.POST:
            form = UserEditForm(instance=self.get_object())
            password_form = PswChangeForm(self.get_object(), self.request.POST,)
            if password_form.is_valid():
                messages.success(self.request, 'User Passsword was updated successfully!')
                password_form.save()
            else:
                messages.error(self.request, 'User Passsword was not updated successfully!')
            return self.render_to_response({'form': form, 'password_form': password_form})

        return super().post(request, *args, **kwargs)


    def form_valid(self, form):
        messages.success(self.request, 'User was updated successfully!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('accounts_urls:users_edit_url', kwargs={'pk': self.kwargs['pk']})

class UserCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'is_staff'
    template_name = 'accounts/user_edit.html'
    form_class = UserCreateForm
    model = MyUser

    def get_context_data(self, **kwargs):
        context = super(UserCreate, self).get_context_data(**kwargs)
        context['action'] = 'create'
        return context

    def form_valid(self, form):
        self.object = form.save()
        from django.contrib.auth.models import Group
        group = Group.objects.get(pk=form.data['groups'])
        self.object.groups.add(group)
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, 'User was created successfully!')
        return reverse_lazy('accounts_urls:users_edit_url', kwargs={'pk': self.object.pk})

class AdminSubjectTransfer(PermissionRequiredMixin, TemplateView):
    permission_required = 'is_staff'
    template_name = 'accounts/user_subject_trasfer.html'

    def get_context_data(self, **kwargs):
        context = super(AdminSubjectTransfer, self).get_context_data(**kwargs)
        context['form'] = AdminRealtyTransferForm
        context['reaty_clients_form'] = AdminClientsTransferForm
        return context

    def post(self, request, *args, **kwargs):
        form = AdminRealtyTransferForm(request.POST)
        reaty_clients_form = AdminClientsTransferForm(request.POST)

        if '_transfer_realty' in request.POST:
            if form.is_valid():
                RealtyEstate.objects.filter(author=form.cleaned_data['author']). \
                    update(author=form.cleaned_data['recipient'])
                messages.success(self.request, 'Relty trasfer complite!')
                return self.render_to_response({'form': form,
                                                'reaty_clients_form':reaty_clients_form})

        if '_transfer_clients' in request.POST:
            if reaty_clients_form.is_valid():
                Client.objects.filter(author=reaty_clients_form.cleaned_data['author']). \
                    update(author=reaty_clients_form.cleaned_data['recipient'])
                messages.success(self.request, 'Clients trasfer complite!')
                return self.render_to_response({'reaty_trasfer_form': form,
                                                'reaty_clients_form':reaty_clients_form})

class QuidesEdit(PermissionRequiredMixin, ModelFormSetView):
    permission_required = 'is_staff'
    template_name = 'accounts/user_subject_list_edit.html'
    action = ''
    exclude = []









