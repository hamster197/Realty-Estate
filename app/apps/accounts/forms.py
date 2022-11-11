from django.utils.translation import gettext_lazy as _

from django.contrib.auth.forms import AuthenticationForm, SetPasswordForm, UserCreationForm
from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Count

from app.apps.accounts.models import MyUser


class LoginForm(AuthenticationForm):
    class Meta:
        model = MyUser
        exclude = []

class PswChangeForm(SetPasswordForm):
    class Meta:
        model = MyUser
        exclude = []

class UserForm(forms.ModelForm):
    first_name = forms.CharField(required=True, label=_('Имя'))
    last_name = forms.CharField(required=True, label=_('Фамилия'))
    email = forms.EmailField(required=True)

    class Meta:
        model = MyUser
        exclude = ['password', 'last_login', 'is_superuser', 'is_active', 'is_staff', 'date_joined',
                   'user_permissions', ]

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        if cleaned_data['groups'].values().count() != 1:
            raise ValidationError(_('Выберите 1 группу(обязательное поле)!'), code='invalid')
        if cleaned_data['groups'].values().filter(name='Риелтор') and cleaned_data['departament']==None:
            raise ValidationError(_('Выберите отдел(обязательное поле)!'), code='invalid')
        if cleaned_data['city']==None and cleaned_data['groups'].values().filter(name='Начальник филиала'):
            raise ValidationError(_('Выберите город для группы Начальник филиала(обязательное поле)!'), code='invalid')

        return cleaned_data

class UserEditForm(UserForm):
    class Meta(UserForm.Meta):
        model = MyUser

class UserCreateForm(UserCreationForm, UserForm):

    class Meta(UserForm.Meta):
        model = MyUser

class UserModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return str(obj) + ' ({})'.format(obj.counter)

class AdminRealtyTransferForm(forms.Form):
    author = UserModelChoiceField(label=_('Перенести обьекты с:'), required=True, queryset=MyUser.objects.all()
                                    .order_by('last_name').annotate(counter=Count('realty_estate_author_id')))
    recipient = UserModelChoiceField(label=_('Перенести обьекты на:'), required=True, queryset=MyUser.objects.all()
                                    .order_by('last_name').annotate(counter=Count('realty_estate_author_id')))


class AdminClientsTransferForm(forms.Form):
    author = UserModelChoiceField(label=_('Перенести клиентов с:'), required=True, queryset=MyUser.objects.all()
                                    .order_by('last_name').annotate(counter=Count('client_author_id')))
    recipient = UserModelChoiceField(label=_('Перенести клиентов на:'), required=True, queryset=MyUser.objects.all()
                                    .order_by('last_name').annotate(counter=Count('client_author_id')))



