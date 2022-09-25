from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, ListView
from django_filters.views import FilterView
from django.contrib import messages

from app.apps.real_estate.filters import RealtyEstateFilter
from app.apps.real_estate.forms import CommerceEditForm, FlatEditForm, HouseEditForm, PlotOfLandEditForm, ClientNewForm
from app.apps.real_estate.models import RealtyEstate, Flat, House, PlotOfLand, Commerce, RealtyEstateGalery, Client


class InstanseSaveMixin(object):
    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.author = self.request.user

        if self.form_class == FlatEditForm:
            instance.type = 'Квартира'
        elif self.form_class == HouseEditForm:
            instance.type = 'Дом'
        elif self.form_class == PlotOfLandEditForm:
            instance.type = 'Участок'
        elif self.form_class == CommerceEditForm:
            instance.type = 'Коммерция'
        instance.save()

        if self.request.FILES.getlist('instance_files'):
            new_pictures_in_galery = []
            for file in self.request.FILES.getlist('instance_files'):
                new_picture_in_galery = RealtyEstateGalery(realty_estate=instance, image=file)
                new_pictures_in_galery.append(new_picture_in_galery)

            galery_instanses = RealtyEstateGalery.objects.bulk_create(new_pictures_in_galery)
            galery_ids = []
            for instance in galery_instanses:
                galery_ids.append(instance.pk)

            from .tasks import galery_watermak
            galery_watermak.apply_async(args=[galery_ids], countdown=40)

        return super().form_valid(form)

class InstanceNew(LoginRequiredMixin, InstanseSaveMixin, CreateView):
    template_name = 'real_estate/instance_new.html'
    success_url = reverse_lazy('real_estates_urls:all_real_estates_url')
    action = 'New '

class InstanceEdit(LoginRequiredMixin, InstanseSaveMixin, UpdateView):
    template_name = 'real_estate/instance_new.html'
    action = 'Edit '

    def get_queryset(self):
        if self.form_class == FlatEditForm:
            self.queryset = Flat.objects.filter(author=self.request.user)
        elif self.form_class == HouseEditForm:
            self.queryset = House.objects.filter(author=self.request.user)
        elif self.form_class == PlotOfLandEditForm:
            self.queryset = PlotOfLand.objects.filter(author=self.request.user)
        elif self.form_class == CommerceEditForm:
            self.queryset = Commerce.objects.filter(author=self.request.user)
        return self.queryset

    def get_initial(self):
        sity_instance = get_object_or_404(RealtyEstate, pk=self.kwargs['pk']).district.city
        return {'city': sity_instance}

    def get_context_data(self, **kwargs):
        context = super(InstanceEdit, self).get_context_data(**kwargs, )
        context['instance'] = get_object_or_404(RealtyEstate, pk=self.kwargs['pk'])
        return context

    def post(self, request, *args, **kwargs):
        if '_delete_image' in self.request.POST:
            RealtyEstateGalery.objects.filter(pk=self.request.POST.get('_delete_image')).delete()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, 'Your instance was updated successfully!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.success(self.request, 'Your instance was not updated successfully!')
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        if self.form_class == FlatEditForm:
            url = reverse_lazy('real_estates_urls:edit_flat_url', kwargs={'pk':self.kwargs['pk']})
        elif self.form_class == HouseEditForm:
            url = reverse_lazy('real_estates_urls:edit_house_url', kwargs={'pk':self.kwargs['pk']})
        elif self.form_class == PlotOfLandEditForm:
            url = reverse_lazy('real_estates_urls:edit_plot_of_land_url', kwargs={'pk':self.kwargs['pk']})
        elif self.form_class == CommerceEditForm:
            url = reverse_lazy('real_estates_urls:edit_commerce_url', kwargs={'pk':self.kwargs['pk']})
        return url


class AllRealEstates(LoginRequiredMixin, FilterView):
    template_name = 'real_estate/instances_all.html'
    filterset_class = RealtyEstateFilter
    context_object_name = 'instances'
    paginate_by = 10

class MyRealtyEstates(LoginRequiredMixin, FilterView):
    template_name = 'real_estate/instances_all.html'
    context_object_name = 'instances'
    paginate_by = 10

class MyRealtyDetail(LoginRequiredMixin, DetailView):
    template_name = 'real_estate/instances_detail.html'
    context_object_name = 'instance'

    def get_queryset(self):
        return RealtyEstate.objects.filter(status_obj='Опубликован')

    def get_context_data(self, **kwargs):
        context = super(MyRealtyDetail, self).get_context_data(**kwargs)
        context['clients'] = Client.objects.filter(estate_type=self.object.type,
            district=self.object.district, status=False,
            min_price__lte=self.object.agency_price, max_price__gte=self.object.agency_price)
        return context

class YandexFeed(ListView):
    template_name = 'real_estate/yandex_feed.html'
    context_object_name = 'instances'

    def get_queryset(self):
        return RealtyEstate.objects.filter(status_obj='Опубликован')

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'instances': self.get_queryset()},
               content_type="text/xml")

class ClientNew(LoginRequiredMixin, CreateView):
    template_name = 'real_estate/client_edit.html'
    form_class = ClientNewForm
    success_url = reverse_lazy('real_estates_urls:client_list_url')
    action = '(New)'

    def form_valid(self, form):
        client  = form.save(commit=False)
        client.author = self.request.user
        client.save()
        messages.success(self.request, 'Your new client was updated successfully!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.success(self.request, 'Your new client was not updated successfully!')
        return self.render_to_response(self.get_context_data(form=form))

class ClientEdit(LoginRequiredMixin, UpdateView):
    template_name = 'real_estate/client_edit.html'
    form_class = ClientNewForm
    action = '(Edit)'

    def get_queryset(self):
        return Client.objects.filter(author=self.request.user)

    def get_initial(self):
        sity_instance = get_object_or_404(RealtyEstate, pk=self.kwargs['pk']).district.city
        return {'city': sity_instance}

    def form_valid(self, form):
        messages.success(self.request, 'Your new client was updated successfully!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.success(self.request, 'Your new client was not updated successfully!')
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        url = reverse_lazy('real_estates_urls:client_edit_url', kwargs={'pk':self.kwargs['pk']})
        return url

class MyClientsList(LoginRequiredMixin, FilterView):
    template_name = 'real_estate/client_list.html'
    context_object_name = 'clients_list'
    action = 'My '
    paginate_by = 10

class AllClientsList(MyClientsList):
    action = 'All  '

class ClientDetail(LoginRequiredMixin, DetailView):
    template_name = 'real_estate/client_detail.html'
    context_object_name = 'client'
    model = Client

    def get_context_data(self, **kwargs):
        context = super(ClientDetail, self).get_context_data(**kwargs)
        context['instances'] = RealtyEstate.objects.filter(type=self.object.estate_type,
            district__in=self.object.district.all(), status_obj='Опубликован',
            agency_price__gt=self.object.min_price, agency_price__lte=self.object.max_price)
        return context




