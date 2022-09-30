
from django.contrib.auth.models import AbstractUser, Group
from django.db import models

# Create your models here.
from app.apps.real_estate.models import CityQuide

class Departament(models.Model):
    city = models.ForeignKey('real_estate.CityQuide', verbose_name='Город', on_delete=models.CASCADE,
                             related_name='departamint_city_id', )
    name = models.CharField(verbose_name='Отдел', max_length=55,)

    def __str__(self):
        return self.name + ' ( ' + str(self.city) + ' )'

    class Meta:
        verbose_name = 'Отдел'
        verbose_name_plural = 'Отделы'
        unique_together = ('city', 'name')

class MyUser(AbstractUser):
    patronymic = models.CharField(verbose_name='Oтчество', max_length=45, blank=False,)
    phone = models.CharField(verbose_name='Телефон', help_text='9881112233', max_length=10,)
    department_boss = models.BooleanField('Начальник отдела', default=False,)
    city = models.ForeignKey(CityQuide, verbose_name='Город(для начальника филиала)', related_name='group_city_id',
                             blank=True, null=True, on_delete=models.CASCADE)
    avatar = models.ImageField(verbose_name='Фото', upload_to='image/%Y/%m/%d/real',
                               default='/static/logo21.png',)
    contract_choises = (('Все', 'Все'), ('Без договора', 'Без договора'),
                        ('Агентский', 'Агентский'), ('Эксклюзив', 'Эксклюзив'))
    contract = models.CharField(max_length=55, verbose_name='Договор', choices=contract_choises,
                                default='Все',)
    departament = models.ForeignKey('accounts.Departament', verbose_name='Отдел', related_name='user_departamint_id',
                                    on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        if self.departament:
            return self.first_name + ' ' + self.last_name +' ' + self.departament.name + '(' + str(self.departament.city) + ')'
        else:
            return self.first_name + ' ' + self.last_name





