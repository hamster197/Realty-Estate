from django.contrib import admin

# Register your models here.
from django.contrib.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin

from app.apps.accounts.models import MyUser, Departament


class DepartamentAdmin(ModelAdmin):
    list_display = ('pk', 'city', 'name', )
    list_filter = ('city',)

admin.site.register(Departament, DepartamentAdmin)

class UserAdmin(UserAdmin):
    list_display = ('pk', 'username', 'first_name', 'last_name', 'email', 'is_superuser', 'is_staff', 'is_active',
                    'last_login',)
    list_editable = ('is_active', 'is_superuser', 'is_staff')
    list_filter = ('is_superuser', 'is_active', 'is_staff', 'last_login', 'departament',)
    fieldsets = (
        (None, {
            'fields': ('username', 'first_name', 'patronymic', 'last_name', 'phone', 'email', 'password',
                       'contract', 'nach_otd', 'groups', 'departament', 'avatar', 'is_active',)
        }),
    )

admin.site.register(MyUser, UserAdmin)