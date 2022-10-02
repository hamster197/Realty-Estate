from django.contrib import admin

# Register your models here.
from app.apps.deals.models import *

admin.site.register(SalesChanelQuide)

class SubmittedCommissionInline(admin.TabularInline):
    model = SubmittedCommission
    readonly_fields = ('commission_date', 'commission_sum')

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

class RealtorInTheDealInline(admin.TabularInline):
    model = RealtorInTheDeal
    readonly_fields = ('name', 'percent', 'realtor_commision_sum',)

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

class DealFields(admin.ModelAdmin):
    inlines = [RealtorInTheDealInline, SubmittedCommissionInline]#
    list_display = ('pk', 'date_open_deal', 'client_name', 'name_of_object', 'client_name', 'price',  'district',
                'status', 'date_close_deal', )
    list_filter = ('status', 'type_of_pbject', 'district', )

admin.site.register(Deal, DealFields)

class DealSystemQuideInline(admin.ModelAdmin):

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(DealSystemQuide, DealSystemQuideInline)
