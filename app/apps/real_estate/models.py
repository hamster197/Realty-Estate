from django.utils.translation import gettext_lazy as _

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MinLengthValidator
from django.db import models

# Create your models here.

class CityQuide(models.Model):
    name = models.CharField(verbose_name=_('Название'), max_length=45, unique=True,)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Город')
        verbose_name_plural = _(' Справочник города')
        ordering = ('name',)

class DistrictQuide(models.Model):
    city = models.ForeignKey('real_estate.CityQuide', verbose_name=_('Город'), on_delete=models.CASCADE,
                             related_name='district_city_id', )
    name = models.CharField(verbose_name=_('Район'), max_length=45,)

    def __str__(self):
        return self.name + ' ( ' + str(self.city) +' )'

    class Meta:
        verbose_name = _('Район')
        verbose_name_plural = _(' Справочник районы')
        unique_together =('city' ,'name')
        ordering = ('city', 'name')

class RealtyEstate(models.Model):
    author = models.ForeignKey('accounts.MyUser', verbose_name=_('Автор'), on_delete=models.CASCADE,
                               related_name='realty_estate_author_id',)
    client_name =  models.CharField(verbose_name=_('Имя собственника'), max_length=50,)
    client_tel = models.CharField(verbose_name=_('тел собственника'), help_text ='+79881234567', max_length=12,)
    creation_date = models.DateField(verbose_name=_('Дата публикации'), auto_now_add=True,)
    date_of_change = models.DateField(verbose_name=_('Дата изменения'), auto_now=True,)
    status_choises = (
        ('Опубликован', _('Опубликован')), ('Не опубликован', _('Не опубликован')), ('В архиве', _('В архиве')))
    status_obj = models.CharField(_('Публикация'), max_length=45, choices=status_choises,)
    contract_choises = (('Без договора', _('Без договора')), ('Агентский', _('Агентский')), ('Эксклюзив', _('Эксклюзив')))
    contract = models.CharField(max_length=55, verbose_name=_('Договор'), choices=contract_choises,
                                default=_('Без договора'),)
    contract_number = models.CharField(max_length=55, verbose_name=_('Номер договора'), default='',)
    contract_date_end = models.DateField(verbose_name=_('До'), null=True, blank=True,)
    new_building = models.BooleanField(verbose_name=_('Новостройка?'), default=False,)
    youtube = models.URLField(verbose_name=_('Код видео с youtube'), max_length=255, blank=True,)
    type_choises = (('Квартира', _('Квартира')), ('Дом', _('Дом')), ('Участок', _('Участок')),
                    ('Коммерция', _('Коммерция')))
    type = models.CharField(max_length=25, verbose_name=_('Тип недвижимости'), choices=type_choises,)
    district = models.ForeignKey(DistrictQuide, verbose_name=_('Район'), on_delete=models.CASCADE,
                                 related_name='realty_estate_district_id', )
    street = models.CharField(max_length=70, verbose_name=_('Улица:'), help_text=_('например: Гагарина'))
    street_number = models.CharField(verbose_name=_('Номер дома(если есть, необязательно к заполнению!):'),
                                  blank=True, max_length=15,)
    latitude = models.CharField(verbose_name=_('latitude'), max_length=255, blank=True,)
    longitude = models.CharField(verbose_name=_('longitude'), max_length=255, blank=True,)
    ploshad = models.DecimalField(verbose_name=_('Площадь(метры)'), decimal_places=2, max_digits=5,)
    owners_price = models.IntegerField(verbose_name=_('Цена собственника'), validators=[MinValueValidator(300000)],)
    agency_price = models.IntegerField(verbose_name=_('Цена агентства'), validators=[MinValueValidator(300000)],)
    discription = models.TextField(verbose_name=_('Описание'), blank=True,)
    gaz_choises = (('Нет',_('Нет')), ('Есть',_('Есть')), ('Можно подключить',_('Можно подключить')),
                 ('В процессе подключения',_('В процессе подключения')))
    gaz = models.CharField('Газ', max_length=40, choices=gaz_choises,)
    cadastral_number = models.CharField(max_length=30, blank=True, verbose_name=_('Кадастровый номер'),
                               help_text=_('Необязательно к заполнению'), validators=[MinLengthValidator(15)],)
    type_of_law_choises = (('Собственность',_('Собственность')), ('Аренда (49лет)',_('Аренда (49лет)')),
                           ('Размещение эллингов',_('Размещение эллингов')))
    type_of_law = models.CharField(max_length=25,  verbose_name=_('Вид права:'), choices=type_of_law_choises,)
    use_of_the_plot_choises = (('Поселений (ИЖС)',_('Поселений (ИЖС)')),
                               ('Садовое некоммерческое товарищество',_('Садовое некоммерческое товарищество')),
                              ('Земля промназначения',_('Земля промназначения')),
                               ('ДНП',_('ДНП')), ('Размещение эллингов',_('Размещение эллингов')))
    use_of_the_plot = models.CharField(max_length=155, verbose_name=_('Использование участка:'),
                                       choices=use_of_the_plot_choises, )
    image = models.ImageField(verbose_name=_('Главное фото'), upload_to='image/%Y/%m/%d/real/main',)

    domclick_pub = models.BooleanField(verbose_name=_('Опубликовать на Домклик'), default=True,)

    def clean(self):
        errors = {}
        if self.owners_price is not None and self.agency_price is not None:
            if (self.owners_price >= self.agency_price):
                errors['owners_price'] = _('the owners price is more than agency price')
        if errors:
            raise ValidationError(errors)

    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name = _('Обьект недвижимости')
        verbose_name_plural = _('Обьекты недвижимости')
        ordering = ['-date_of_change', '-pk']

class RealtyEstateGalery(models.Model):
    realty_estate = models.ForeignKey('real_estate.RealtyEstate', verbose_name=_('Обьект недвижимости'),
                                      related_name='galery_real_estate_id', on_delete=models.CASCADE)
    image = models.ImageField(verbose_name=_('Картинка'), upload_to='image/%Y/%m/%d/real/main',)

    def __str__(self):
        return self.image.url
    class Meta:
        verbose_name = _('Галерея')
        verbose_name_plural = _('Галерея')



class Flat(RealtyEstate):
    flat_number = models.CharField(verbose_name=_('Номер квартиры (необязательное поле):'), help_text=_('например: 11'),
                                   max_length=5, blank=True,)
    stage_of_delivery_choises = (('Не сдан',_('Не сдан')), ('Рег.УФРС',_('Рег.УФРС')), ('ФЗ-214',_('ФЗ-214')),
                                 ('ФЗ-215',_('ФЗ-215')), ('Сдан',_('Сдан')))
    stage_of_delivery = models.CharField(verbose_name=_('Этап сдачи'), max_length=40, choices=stage_of_delivery_choises,)

    housing_status_choises= (('Жилое помещение',_('Жилое помещение')),
          ('Нежилое помещение((Апартаменты, подвал, коммерция))',_('Нежилое помещение((Апартаменты, подвал, коммерция))')),
          ('Часть жил.дома',_('Часть жил.дома')), ('Квартира',_('Квартира')), ('Комната',_('Комната')))
    housing_status = models.CharField('Статус жилья',max_length=140,choices=housing_status_choises,)

    housing_class_choises = (('Эконом',_('Эконом')), ('Комфорт',_('Комфорт')), ('Бизнес',_('Бизнес')), ('Элит',_('Элит')))
    housing_class = models.CharField(verbose_name=_('Класс жилья'), max_length=45,choices=housing_class_choises,)

    repair_choises = (('Черновой',_('Черновой')), ('Чистовой',_('Чистовой')), ('Дизайнерский',_('Дизайнерский')),
                      ('Жилой',_('Жилой')),  ('Новый',_('Новый')), ('Косметический',_('Косметический')),
                      ('Евроремонт',_('Евроремонт')),)
    repair = models.CharField(verbose_name=_('Ремонт'), max_length=25, choices=repair_choises,)

    rooms_choises = (('Студия', _('Студия')), ('Однокомнатная', _('Однокомнатная')), ('Двухкомнатная', _('Двухкомнатная')),
                    ('Трехкомнатная', _('Трехкомнатная')), ('Многокомнатная', _('Многокомнатная')))
    rooms = models.CharField(verbose_name=_('Кол-во комнат'), max_length=25, choices=rooms_choises,)

    floor = models.IntegerField(verbose_name=_('Этаж'), default=1)
    number_of_floors = models.IntegerField(verbose_name=_('Этажность'), default=1)

    view_from_the_windows_choises = (
    ('Обычный', _('Обычный')), ('На стену', _('На стену')), ('На море', _('На море')), ('На горы', _('На горы')),
    ('Во двор', _('Во двор')), ('На улицу', _('На улицу')), ('На две стороны ', _('На две стороны ')),)
    view_from_the_windows = models.CharField(verbose_name=_('Вид из окон'), max_length=25,
                                             choices=view_from_the_windows_choises,)

    bathroom_choises = (('Совмещенный', _('Совмещенный')), ('Раздельный', _('Раздельный')))
    bathroom = models.CharField(verbose_name=_('Санузел'), max_length=15, choices=bathroom_choises,)

    parking_choises = (('Есть', _('Есть')), ('Нет', _('Нет')), ('Подземный', _('Подземный')),)
    parking = models.CharField(verbose_name=_('Паркинг'), max_length=15, choices=parking_choises,)
    security = models.BooleanField(verbose_name=_('Наличие охраны:'), default=False,)
    rubbish_chute = models.BooleanField(verbose_name=_('Мусоропровод:'), default=False,)
    elevator = models.BooleanField(verbose_name=_('Лифт:'), default=False,)

    bch = (('да', _('да')), ('нет', _('нет')), ('2 балкона', _('2 балкона')), ('1 лоджия', _('1 лоджия')),
           ('2 лоджии', _('2 лоджии')), )
    balcony = models.CharField(max_length=15, choices=bch, verbose_name=_('Балкон:'), default=_('нет',))

    def clean(self):
        errors = {}
        if self.floor is not None and self.number_of_floors is not None:
            if (self.floor > self.number_of_floors):
                errors['floor'] = _('the floor is more than number of floors')
        if errors:
            raise ValidationError(errors)
    class Meta:
        verbose_name = _('Квартира')
        verbose_name_plural = _('Квартиры')

class House(RealtyEstate):
    number_of_floors_choises = (('1','1'),('2','2'),('3','3'),('4','4'),('5','5'),('6','6'))
    number_of_floors = models.CharField(max_length=1, verbose_name=_('Этажность:'), choices=number_of_floors_choises,)

    number_of_flats_choises = (('1','1'),('2','2'),('3','3'),('4','4'),('5','5'),('6','6'),('7','7'),('8','8'),('9','9'),('10','10'),
                        ('11','11'),('12','12'),('13','13'),('14','14'),('15','15'),('16','16'),('17','17'),('18','18'),
                        ('19','19'),('20','20'),)
    number_of_flats = models.CharField(max_length=3, verbose_name=_('Комнат:'), choices=number_of_flats_choises,)

    type_of_house_choises = (('Монолитный',_('Монолитный')), ('Блочный',_('Блочный')), ('Каркасно-монолитный',_('Каркасно-монолитный')),
                          ('Кирпичный',_('Кирпичный')), ('Деревянный',_('Деревянный')), ('Панельный',_('Панельный')),
                          ('Монолитно-кирпичный',_('Монолитно-кирпичный')))
    type_of_house = models.CharField(max_length=25, verbose_name=_('Тип дома'), choices=type_of_house_choises,)

    plot_area = models.IntegerField(default='0',  verbose_name=_('Площадь участка (В МЕТРАХ!)'))

    class Meta:
        verbose_name = _('Дом')
        verbose_name_plural = _('Дома')

class PlotOfLand(RealtyEstate):
    relief_choises = (('Ровный', _('Ровный')), ('Уклон', _('Уклон')))
    relief = models.CharField(verbose_name=_('Вид рельефа:'), max_length=25, choices=relief_choises, )
    view_choises = (('На море', _('На море')), ('На горы', _('На горы')), ('На море и горы', _('На море и горы')))
    view = models.CharField(verbose_name=_('Вид'), max_length=25, choices=view_choises)

    class Meta:
        verbose_name = _('Участок')
        verbose_name_plural = _('Участки')

class Commerce(RealtyEstate):
    type_of_building_choises = (('Торговое помещение', _('Торговое помещение')),
                             ('Помещение Свободного назначения', _('Помещение Свободного назначения')),
                             ('Склад', _('Склад')), ('Офисное помещение', _('Офисное помещение')),
                             ('Производство', _('Производство')),
                             ('Другая коммерческая недвижимость', _('Другая коммерческая недвижимость')),
                             )
    type_of_building = models.CharField(verbose_name=_('Тип строения'), max_length=80, choices=type_of_building_choises,)
    type_deal_choises = (('аренда', _('аренда')), ('продажа', _('продажа')),)
    type_deal = models.CharField(verbose_name=_('Тип Сделки'), max_length=80, choices=type_deal_choises,)

    class Meta:
        verbose_name = _('Коммерция')
        verbose_name_plural = _('Коммерция')

class Client(models.Model):
    creation_date = models.DateField(verbose_name=_('Дата создания'), auto_now_add=True)
    author = models.ForeignKey('accounts.MyUser', verbose_name=_('Автор'), related_name='client_author_id',
                               on_delete=models.CASCADE)
    status = models.BooleanField(verbose_name=_('Клиент закрыт'), default=False)
    client_name = models.CharField(max_length=45, verbose_name=_('Клиент(ФИО)'))
    phone = models.CharField(verbose_name=_('Телефон клиента'), help_text='9881112233', max_length=10,)
    email = models.EmailField(verbose_name=_('email клиента'), default='nomail@nomail.ru')
    estate_type = models.CharField(verbose_name=_('Что ищет'), max_length=45, choices=RealtyEstate.type_choises)
    district = models.ManyToManyField(DistrictQuide, verbose_name=_('Район'), related_name='client_distinkt_id',)
    discription = models.TextField(verbose_name=_('Примечание'))
    min_price = models.IntegerField(verbose_name=_('Бюджет от:'), validators=[MinValueValidator(300000)])
    max_price = models.IntegerField(verbose_name=_('Бюджет до:'), validators=[MinValueValidator(300000)])

    def __str__(self):
        return self.client_name

    def clean(self):
        errors = {}
        if self.min_price is not None and self.max_price is not None:
            if (self.min_price >= self.max_price):
                errors['min_price'] = _('the min price is more than max price')
        if errors:
            raise ValidationError(errors)
    class Meta:
        verbose_name = _(' Клиенты')
        verbose_name_plural = _(' Клиенты')