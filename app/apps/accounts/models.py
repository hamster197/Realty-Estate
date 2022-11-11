from django.utils.translation import gettext_lazy as _

from django.contrib.auth.models import AbstractUser, Group
from django.db import models

# Create your models here.
from app.apps.real_estate.models import CityQuide

class Departament(models.Model):
    city = models.ForeignKey('real_estate.CityQuide', verbose_name=_('Город'), on_delete=models.CASCADE,
                             related_name='departamint_city_id', )
    name = models.CharField(verbose_name=_('Отдел'), max_length=55,)

    def __str__(self):
        return self.name + ' ( ' + str(self.city) + ' )'

    class Meta:
        verbose_name = _('Отдел')
        verbose_name_plural = _('Отделы')
        unique_together = ('city', 'name')
        ordering = ('city', 'name')

class MyUser(AbstractUser):
    patronymic = models.CharField(verbose_name=_('Oтчество'), max_length=45, blank=False,)
    phone = models.CharField(verbose_name=_('Телефон'), help_text='9881112233', max_length=10,)
    department_boss = models.BooleanField(_('Начальник отдела'), default=False,)
    city = models.ForeignKey(CityQuide, verbose_name=_('Город(для начальника филиала)'), related_name='group_city_id',
                             blank=True, null=True, on_delete=models.CASCADE)
    avatar = models.ImageField(verbose_name=_('Фото'), upload_to='image/%Y/%m/%d/real',
                               default='/static/logo21.png',)
    contract_choises = (('Все', _('Все')), ('Без договора', _('Без договора')),
                        ('Агентский', _('Агентский')), ('Эксклюзив', _('Эксклюзив')))
    contract = models.CharField(max_length=55, verbose_name=_('Договор'), choices=contract_choises,
                                default='Все',)
    departament = models.ForeignKey('accounts.Departament', verbose_name=_('Отдел'), related_name='user_departamint_id',
                                    on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')

    def __str__(self):
        if self.departament:
            return self.first_name + ' ' + self.last_name +' ' + self.departament.name + '(' + str(self.departament.city) + ')'
        else:
            return self.first_name + ' ' + self.last_name





