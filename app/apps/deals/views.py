
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils import timezone

# Create your views here.
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django_filters.views import FilterView

from app.apps.deals.core import OpenDealList, AllDealsCounter
from app.apps.deals.filters import DealClosedFilter, DealInstallmentClosedFilter, DealDisruptionFilter
from app.apps.deals.forms import DealFormset, DealEditForm, DealCommissionFormset
from app.apps.deals.models import RealtorInTheDeal
from app.apps.real_estate.models import RealtyEstate


class DealsOpenList(LoginRequiredMixin, ListView):
    template_name = 'deals/dials_list.html'
    context_object_name = 'instances'
    deal_status = ''

    def get_queryset(self):
        deal_status = []
        deal_status.append(self.deal_status)
        return OpenDealList(self.request.user, deal_status)

    def get_context_data(self, **kwargs):
        context = super(DealsOpenList, self).get_context_data(**kwargs)
        start_date = timezone.now().replace(hour=0, minute=0, second=0, day=1)
        end_date = timezone.now().replace(hour=23, minute=59, second=59)
        context['rezult_string'] = AllDealsCounter(start_date, end_date)
        return context


class DealsNotOpenList(LoginRequiredMixin, FilterView):
    template_name = 'deals/dials_list.html'
    context_object_name = 'instances'

    def get_context_data(self, **kwargs):
        context = super(DealsNotOpenList, self).get_context_data(**kwargs)
        if self.filterset_class == DealClosedFilter:
            context['deal_status'] = 'Закрыта'
        elif self.filterset_class == DealInstallmentClosedFilter:
            context['deal_status'] = 'Закрыта-Рассрочка'
        elif self.filterset_class == DealDisruptionFilter:
            context['deal_status'] = 'Срыв'
            #self.get_filterset_kwargs()

        start_date = timezone.now().replace(hour=0, minute=0, second=0, day=1)
        end_date = timezone.now().replace(hour=23, minute=59, second=59)
        if self.get_filterset_kwargs(self.filterset_class).get('data'):
            if self.get_filterset_kwargs(self.filterset_class).get('data').get('date_close_deal_min'):
                start_date = self.get_filterset_kwargs(self.filterset_class).get('data').get('date_close_deal_min')
            if self.get_filterset_kwargs(self.filterset_class).get('data').get('date_close_deal_max'):
                end_date = self.get_filterset_kwargs(self.filterset_class).get('data').get('date_close_deal_max')
        context['rezult_string'] = AllDealsCounter(start_date, end_date)

        return context

class DealDetail(LoginRequiredMixin, DetailView):
    template_name = 'deals/dials_detail.html'
    context_object_name = 'instance'

    def get_queryset(self):
        deal_status = ['Закрыта', 'Закрыта-Рассрочка', 'Открыта', 'Срыв', 'Рассрочка', ]
        return OpenDealList(self.request.user, deal_status)

    def post(self, request, *args, **kwargs):
        object = super(DealDetail, self).get_object()
        if '_close' in self.request.POST:
            object.status = 'Закрыта'
        elif '_disruption' in self.request.POST:
            object.status = 'Закрыта-Рассрочка'
        object.save()
        return redirect('deal_urls:deal_detail_url', pk=self.get_object().pk)

class DealNew(LoginRequiredMixin, CreateView):
    form_class = DealEditForm
    action = '(New)'
    template_name = 'deals/dials_new.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        self.object = form.save()
        RealtorInTheDeal.objects.create(deal=self.object, name=self.request.user, percent=10)
        return super().form_valid(form)

    def get_success_url(self):
        url = reverse_lazy('deal_urls:deal_edit_url', kwargs={'pk': self.object.pk})
        return url

class DealEdit(LoginRequiredMixin, UpdateView):
    form_class = DealEditForm
    template_name = 'deals/dials_new.html'

    def get_queryset(self):
        deal_status = ['Закрыта-Рассрочка', 'Открыта', 'Рассрочка', ]
        return OpenDealList(self.request.user, deal_status)

    def get_initial(self):
        sity_instance = get_object_or_404(RealtyEstate, pk=self.kwargs['pk']).district.city
        return {'city': sity_instance}

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(DealEdit, self).get_context_data(**kwargs)
        if self.request.POST:
            context['deal_realtors_formset'] = DealFormset(self.request.POST, instance=self.object)
            if self.request.user.groups.get().name != 'Риелтор':
                context['deal_commision_formset'] = DealCommissionFormset(self.request.POST, instance=self.object)
        else:
            context['deal_realtors_formset'] = DealFormset(instance=self.object)
            if self.request.user.groups.get().name != 'Риелтор':
                context['deal_commision_formset'] = DealCommissionFormset(instance=self.object)
        context['action'] = '(Edit)'
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        deal_realtors_formset = DealFormset(self.request.POST, instance=self.object)
        deal_commision_formset = DealCommissionFormset(self.request.POST, instance=self.object)

        if self.request.user.groups.get().name != 'Риелтор':
            if form.is_valid() and deal_realtors_formset.is_valid() and deal_commision_formset.is_valid():
                return self.form_valid(form, deal_realtors_formset, deal_commision_formset)
            else:
                return self.form_invalid(form, deal_realtors_formset, deal_commision_formset)

        if self.request.user.groups.get().name == 'Риелтор':
            if form.is_valid() and deal_realtors_formset.is_valid():
                return self.form_valid(form, deal_realtors_formset, deal_commision_formset)
            else:
                return self.form_invalid(form, deal_realtors_formset, deal_commision_formset)

    def form_valid(self, form, deal_realtors_formset, deal_commision_formset):
        messages.success(self.request, 'Your instance was updated successfully!')
        form.save()
        deal_realtors_formset.save()
        deal_commision_formset.save()
        return self.render_to_response(self.get_context_data(form=form, deal_realtors_formset=deal_realtors_formset,
                                                             deal_commision_formset=deal_commision_formset))

    def form_invalid(self, form, deal_realtors_formset, deal_commision_formset):
        messages.success(self.request, 'Your instance was not updated successfully!')
        return self.render_to_response(self.get_context_data(form=form, deal_realtors_formset=deal_realtors_formset,
                                                             deal_commision_formset=deal_commision_formset))

    def get_success_url(self):
        return reverse_lazy('deal_urls:deal_edit_url', kwargs={'pk':self.kwargs['pk']})

class DealReiting(LoginRequiredMixin, FilterView):
    template_name = 'deals/deals_reiting.html'
    context_object_name = 'instances'

