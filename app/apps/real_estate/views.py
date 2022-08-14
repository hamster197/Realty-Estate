from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, ListView, TemplateView
from django_filters.views import FilterView

from app.apps.real_estate.filters import RealtyEstateFilter
from app.apps.real_estate.forms import CommerceEditForm, FlatEditForm, HouseEditForm, PlotOfLandEditForm
from app.apps.real_estate.models import RealtyEstate, Flat, House, PlotOfLand, Commerce, RealtyEstateGalery


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

            for instance in galery_instanses:
                instance.save()

        return super().form_valid(form)

class InstanceNew(LoginRequiredMixin, InstanseSaveMixin, CreateView):
    template_name = 'real_estate/instance_new.html'
    success_url = reverse_lazy('real_estates_urls:all_real_estates_url')

class InstanceEdit(LoginRequiredMixin, InstanseSaveMixin, UpdateView):
    template_name = 'real_estate/instance_new.html'
    success_url = reverse_lazy('real_estates_urls:all_real_estates_url')

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

    def get_context_data(self, **kwargs):
        context = super(InstanceEdit, self).get_context_data(**kwargs)
        context['instance'] = get_object_or_404(RealtyEstate, pk=self.kwargs['pk'])
        return context

    def post(self, request, *args, **kwargs):
        if '_delete_image' in self.request.POST:
            RealtyEstateGalery.objects.filter(pk=self.request.POST.get('_delete_image')).delete()
        return super().post(request, *args, **kwargs)

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

class YandexFeed(ListView):
    template_name = 'real_estate/yandex_feed.html'
    context_object_name = 'instances'

    def get_queryset(self):
        return RealtyEstate.objects.filter(status_obj='Опубликован')

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'instances': self.get_queryset()},
               content_type="text/xml")
