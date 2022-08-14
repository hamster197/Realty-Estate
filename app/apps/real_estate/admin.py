from django.contrib import admin

# Register your models here.
from django.contrib.admin import ModelAdmin

from app.apps.real_estate.models import CityQuide, DistrictQuide, Flat, House, PlotOfLand, Commerce, RealtyEstateGalery

admin.site.register(CityQuide)

class DistrictQuideFields(ModelAdmin):
    list_display = ('pk', 'name', 'city',)
    list_filter = ('city',)

admin.site.register(DistrictQuide, DistrictQuideFields)

class RealtyEstateGaleryAdmin(admin.StackedInline):
    model = RealtyEstateGalery

class EstateFields(ModelAdmin):
    inlines = [RealtyEstateGaleryAdmin]
    list_display = ('pk', 'get_first_name', 'get_last_name', 'type', 'district', 'street', 'ploshad', 'agency_price')
    list_filter = ('author', 'status_obj',)

    def get_first_name(self, obj):
        return obj.author.first_name
    get_first_name.short_description = 'Имя'

    def get_last_name(self, obj):
        return obj.author.last_name
    get_last_name.short_description = 'Фамилия'

admin.site.register(Flat, EstateFields)

admin.site.register(House, EstateFields)

admin.site.register(PlotOfLand, EstateFields)

admin.site.register(Commerce, EstateFields)

class RealtyEstateGaleryFields(ModelAdmin):
    list_display = ('pk', 'realty_estate', 'image', )
    list_filter = ('realty_estate', )

admin.site.register(RealtyEstateGalery, RealtyEstateGaleryFields)