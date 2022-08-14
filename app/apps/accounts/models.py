
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.



class Departament(models.Model):
    city = models.ForeignKey('real_estate.CityQuide', verbose_name='Город', on_delete=models.CASCADE,
                             related_name='departamint_city_id', )
    name = models.CharField(verbose_name='Отдел', max_length=55,)

    def __str__(self):
        return self.name + ' ( ' + str(self.city) + ' )'

    class Meta:
        verbose_name = 'Отдел'
        verbose_name_plural = 'Отделы'

class MyUser(AbstractUser):
    patronymic = models.CharField(verbose_name='Oтчество', max_length=45, blank=False,)
    phone = models.CharField(verbose_name='Телефон', help_text='9881112233', max_length=10,)
    nach_otd = models.BooleanField('Начальник отдела', default=False,)
    avatar = models.ImageField(verbose_name='Фото', upload_to='image/%Y/%m/%d/real',
                               default='/static/logo21.png',)
    contract_choises = (('Все', 'Все'), ('Без договора', 'Без договора'),
                        ('Агентский', 'Агентский'), ('Эксклюзив', 'Эксклюзив'))
    contract = models.CharField(max_length=55, verbose_name='Договор', choices=contract_choises,
                                default='Все',)

    departament = models.ForeignKey('accounts.Departament', verbose_name='Отдел', related_name='user_departamint_id',
                                    on_delete=models.CASCADE,  )
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.first_name + ' ' + self.last_name