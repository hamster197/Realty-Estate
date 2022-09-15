from django.core.validators import MinValueValidator
from django.db import models

# Create your models here.
from django.shortcuts import get_object_or_404

from app.apps.accounts.models import MyUser
from app.apps.real_estate.models import RealtyEstate, DistrictQuide

class DealSystemQuide(models.Model):
    agency_commision_percent = models.IntegerField(verbose_name='Коммисия агенства',)

    class Meta:
       verbose_name = 'Настройки сделок'
       verbose_name_plural = 'Настройки сделок'

class SalesChanelQuide(models.Model):
    name = models.CharField(verbose_name='Kанал продаж', max_length=45)

    def __str__(self):
        return self.name

    class Meta:
       verbose_name = 'Канал продаж'
       verbose_name_plural = 'Каналы продаж'

class Deal(models.Model):
    date_open_deal = models.DateField(verbose_name='Дата создания сделки', auto_now_add=True)
    date_close_deal = models.DateField(verbose_name='Дата закрытия сделки', auto_now=True)
    name_of_object = models.CharField(max_length=140, verbose_name='Название объекта', )
    type_of_pbject = models.CharField(max_length=25, verbose_name='Тип недвижимости', choices=RealtyEstate.type_choises,
                                      )
    district = models.ForeignKey(DistrictQuide, verbose_name='Район', on_delete=models.CASCADE,
                                 related_name='deal_estate_district_id', blank=True, null=True)
    client_name = models.CharField(max_length=50, verbose_name='ФИО клиента(Покупатель)')
    client_phone = models.CharField(verbose_name='тел.Клиента(Покупатель)', help_text='(+79881234567)', blank=False,
                              max_length=20)
    seller_name = models.CharField(max_length=50, verbose_name='ФИО клиента(Продавца)', blank=False, default='')
    seller_phone = models.CharField(verbose_name='тел.Клиента(Продавца)',blank=False,  help_text='(+79881234567)',
                              max_length=20)
    brokers_name = models.CharField(max_length=50, verbose_name='ФИО Посрединка(ч.риелт или др аг.)',
                                 help_text=' если есть',blank=True,)
    brokers_tel = models.CharField(verbose_name='Тел.посредника', help_text='(+79881234567), если есть', blank=True,
                                   max_length=20)
    name_agency = models.CharField(max_length=50, verbose_name='Название агенства',
                                   help_text='если есть',blank=True, )
    sales_chanel = models.ForeignKey(SalesChanelQuide, verbose_name='Kанал продаж', related_name='deal_sales_chanel_id',
                                     on_delete=models.CASCADE)
    square = models.DecimalField(verbose_name='Площадь', decimal_places=2, max_digits=8,
                                  validators=[MinValueValidator(5)], help_text='min 5')
    price = models.IntegerField(verbose_name='Стоимость объекта', validators=[MinValueValidator(300000)],
                                   help_text='min 300 000', )
    commission = models.IntegerField(verbose_name='Комисия', validators=[MinValueValidator(1000)], help_text='min 1 000',)
    mortgage = models.BooleanField(verbose_name='Ипотека', default=False)
    installment = models.BooleanField(verbose_name='Расрочка', default=False)
    discription = models.CharField(max_length=1050, verbose_name='Примечание', blank=True)
    status_choises = (('Закрыта','Закрыта'), ('Закрыта-Рассрочка','Закрыта-Рассрочка'), ('Открыта','Открыта'),
                      ('Срыв','Срыв'), ('Рассрочка','Рассрочка'))
    status = models.CharField(max_length=23, choices=status_choises, default='Открыта', verbose_name='Статус сделки')

    class Meta:
       verbose_name = 'Сделка'
       verbose_name_plural = 'Сделки'

    def save(self, *args, **kwargs):
        agency_commision = get_object_or_404(DealSystemQuide, pk=1).agency_commision_percent
        all_realtor_commision = (self.commission * agency_commision) / 100
        from django.db.models import F
        RealtorInTheDeal.objects.filter(deal=self)\
            .update(realtor_commision_sum=(all_realtor_commision * F('percent')) / 100)
        super(Deal, self).save(*args, **kwargs)


class RealtorInTheDeal(models.Model):
    deal = models.ForeignKey(Deal, verbose_name='Сделка', related_name='realtor_in_deal_deal_id', on_delete=models.CASCADE)
    name = models.ForeignKey(MyUser, verbose_name='Риелтор в сделке', related_name='realtor_in_deal_raltor_id',
                                                                                     on_delete=models.CASCADE, )
    percent = models.IntegerField(verbose_name='Процент в сделке', validators=[MinValueValidator(1)], help_text='min 1%')
    realtor_commision_sum = models.FloatField(verbose_name='сумма коммисии')

    class Meta:
       verbose_name = 'Bсе риелторы в сделке'
       verbose_name_plural = 'Bсе риелторы в сделке'

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        agency_commision = get_object_or_404(DealSystemQuide, pk=1).agency_commision_percent
        all_realtor_commision = (self.deal.commission * agency_commision) / 100
        self.realtor_commision_sum = (all_realtor_commision * self.percent) / 100
        super(RealtorInTheDeal, self).save(*args, **kwargs)

class SubmittedCommission(models.Model):
    deal = models.ForeignKey(Deal, verbose_name='Сделка', related_name='commision_deal_id', on_delete=models.CASCADE)
    commission_sum = models.IntegerField(verbose_name='Внесенно комисии', )
    commission_date = models.DateField(verbose_name='Дата внесения комисии', auto_now_add=True)

    class Meta:
       verbose_name = 'Комисия'
       verbose_name_plural = 'Комисия'