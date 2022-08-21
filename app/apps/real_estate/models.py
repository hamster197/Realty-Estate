from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MinLengthValidator
from django.db import models

# Create your models here.

class CityQuide(models.Model):
    name = models.CharField(verbose_name='Название', max_length=45,)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = ' Справочник города'

class DistrictQuide(models.Model):
    city = models.ForeignKey('real_estate.CityQuide', verbose_name='Город', on_delete=models.CASCADE,
                             related_name='district_city_id', )
    name = models.CharField(verbose_name='Район', max_length=45,)

    def __str__(self):
        return self.name + ' ( ' + str(self.city) +' )'

    class Meta:
        verbose_name = 'Район'
        verbose_name_plural = ' Справочник районы'
        unique_together =('city' ,'name')

class RealtyEstate(models.Model):
    author = models.ForeignKey('accounts.MyUser', verbose_name='Автор', on_delete=models.CASCADE,
                               related_name='realty_estate_author_id',)
    client_name=models.CharField('Имя собственника', max_length=50,)
    client_tel = models.CharField(verbose_name='тел собственника', help_text ='+79881234567', max_length=12,)
    creation_date = models.DateField('Дата публикации', auto_now_add=True,)
    date_of_change = models.DateField('Дата изменения', auto_now=True,)
    status_choises = (
        ('Опубликован', 'Опубликован'), ('Не опубликован', 'Не опубликован'), ('В архиве', 'В архиве'))
    status_obj = models.CharField('Публикация', max_length=45, choices=status_choises,)
    contract_choises = (('Без договора', 'Без договора'), ('Агентский', 'Агентский'), ('Эксклюзив', 'Эксклюзив'))
    contract = models.CharField(max_length=55, verbose_name='Договор', choices=contract_choises,
                                default='Без договора',)
    contract_number = models.CharField(max_length=55, verbose_name='Номер договора', default='',)
    contract_date_end = models.DateField(verbose_name='До', null=True, blank=True,)
    new_building = models.BooleanField(verbose_name='Новостройка?', default=False,)
    youtube = models.URLField(verbose_name='Код видео с youtube', max_length=255, blank=True,)
    type_choises = (('Квартира', 'Квартира'), ('Дом', 'Дом'), ('Участок', 'Участок'),
                    ('Коммерция', 'Коммерция'))
    type = models.CharField(max_length=25, verbose_name='Тип недвижимости', choices=type_choises,)
    district = models.ForeignKey(DistrictQuide, verbose_name='Район', on_delete=models.CASCADE,
                                 related_name='realty_estate_district_id', )
    street = models.CharField(max_length=70, verbose_name='Улица:', help_text='например: Гагарина')
    street_number = models.CharField(verbose_name='Номер дома(если есть, необязательно к заполнению!):',
                                  blank=True, max_length=15,)
    latitude = models.CharField(verbose_name='latitude', max_length=255, blank=True,)
    longitude = models.CharField(verbose_name='longitude', max_length=255, blank=True,)
    ploshad = models.DecimalField(verbose_name='Площадь(метры)', decimal_places=2, max_digits=5,)
    owners_price = models.IntegerField('Цена собственника', validators=[MinValueValidator(300000)],)
    agency_price = models.IntegerField('Цена агентства', validators=[MinValueValidator(300000)],)
    discription = models.TextField('Описание', blank=True,)
    gaz_choises = (('No','Нет'), ('Yes','Есть'), ('Can connect','Можно подключить'),
                 ('В процессе подключения','В процессе подключения'))
    gaz = models.CharField('Газ', max_length=40, choices=gaz_choises,)
    cadastral_number = models.CharField(max_length=30, blank=True, verbose_name='Кадастровый номер',
                               help_text='Необязательно к заполнению', validators=[MinLengthValidator(15)],)
    type_of_law_choises = (('Собственность','Собственность'), ('Аренда (49лет)','Аренда (49лет)'),
                           ('Размещение эллингов','Размещение эллингов'))
    type_of_law = models.CharField(max_length=25,  verbose_name='Вид права:', choices=type_of_law_choises,)
    use_of_the_plot_choises = (('Поселений (ИЖС)','Поселений (ИЖС)'),
                               ('Садовое некоммерческое товарищество','Садовое некоммерческое товарищество'),
                              ('Земля промназначения','Земля промназначения'),
                               ('ДНП','ДНП'), ('Размещение эллингов','Размещение эллингов'))
    use_of_the_plot = models.CharField(max_length=155, verbose_name='Использование участка:',
                                       choices=use_of_the_plot_choises, )
    image = models.ImageField(verbose_name='Главное фото', upload_to='image/%Y/%m/%d/real/main',)

    domclick_pub = models.BooleanField(verbose_name='Опубликовать на Домклик', default=True,)

    def clean(self):
        errors = {}
        if self.owners_price is not None and self.agency_price is not None:
            if (self.owners_price >= self.agency_price):
                errors['owners_price'] = 'the owners price is more than agency price'
        if errors:
            raise ValidationError(errors)

    class Meta:
        verbose_name = 'Обьект недвижимости'
        verbose_name_plural = 'Обьекты недвижимости'
        ordering = ['-date_of_change', '-pk']

    def __str__(self):
        return str(self.pk)

class RealtyEstateGalery(models.Model):
    realty_estate = models.ForeignKey('real_estate.RealtyEstate', verbose_name='Обьект недвижимости',
                                      related_name='galery_real_estate_id', on_delete=models.CASCADE)
    image = models.ImageField(verbose_name='Картинка', upload_to='image/%Y/%m/%d/real/main',)

    class Meta:
        verbose_name = 'Галерея'
        verbose_name_plural = 'Галерея'



class Flat(RealtyEstate):
    flat_number = models.CharField(verbose_name='Номер квартиры (необязательное поле):', help_text='например: 11',
                                   max_length=5, blank=True,)
    stage_of_delivery_choises = (('Не сдан','Не сдан'), ('Рег.УФРС','Рег.УФРС'), ('ФЗ-214','ФЗ-214'), ('ФЗ-215','ФЗ-215'),
                        ('Сдан','Сдан'))
    stage_of_delivery = models.CharField('Этап сдачи',max_length=40,choices=stage_of_delivery_choises,)

    housing_status_choises= (('Жилое помещение','Жилое помещение'),
          ('Нежилое помещение((Апартаменты, подвал, коммерция))','Нежилое помещение((Апартаменты, подвал, коммерция))'),
          ('Часть жил.дома','Часть жил.дома'), ('Квартира','Квартира'), ('Комната','Комната'))
    housing_status = models.CharField('Статус жилья',max_length=140,choices=housing_status_choises,)

    housing_class_choises = (('Эконом','Эконом'), ('Комфорт','Комфорт'), ('Бизнес','Бизнес'), ('Элит','Элит'))
    housing_class = models.CharField('Класс жилья', max_length=45,choices=housing_class_choises,)

    repair_choises = (('Черновой','Черновой'), ('Чистовой','Чистовой'), ('Дизайнерский','Дизайнерский'), ('Жилой','Жилой'),
                    ('Новый','Новый'), ('Косметический','Косметический'), ('Евроремонт','Евроремонт'),)
    repair = models.CharField('Ремонт',max_length=25,choices=repair_choises,)

    rooms_choises = (('Студия', 'Студия'), ('Однокомнатная', 'Однокомнатная'), ('Двухкомнатная', 'Двухкомнатная'),
                    ('Трехкомнатная', 'Трехкомнатная'), ('Многокомнатная', 'Многокомнатная'))
    rooms = models.CharField('Кол-во комнат', max_length=25, choices=rooms_choises,)

    floor = models.IntegerField('Этаж', default=1)
    number_of_floors = models.IntegerField('Этажность', default=1)

    view_from_the_windows_choises = (
    ('Обычный', 'Обычный'), ('На стену', 'На стену'), ('На море', 'На море'), ('На горы', 'На горы'),
    ('Во двор', 'Во двор'), ('На улицу', 'На улицу'), ('На две стороны ', 'На две стороны '),)
    view_from_the_windows = models.CharField('Вид из окон', max_length=25, choices=view_from_the_windows_choises,)

    bathroom_choises = (('Совмещенный', 'Совмещенный'), ('Раздельный', 'Раздельный'))
    bathroom = models.CharField('Санузел', max_length=15, choices=bathroom_choises,)

    parking_choises = (('Есть', 'Есть'), ('Нет', 'Нет'), ('Подземный', 'Подземный'),)
    parking = models.CharField('Паркинг', max_length=15, choices=parking_choises,)
    security = models.BooleanField(verbose_name='Наличие охраны:', default=False,)
    rubbish_chute = models.BooleanField(verbose_name='Мусоропровод:', default=False,)
    elevator = models.BooleanField(verbose_name='Лифт:', default=False,)

    bch = (('да', 'да'), ('нет', 'нет'), ('2 балкона', '2 балкона'), ('1 лоджия', '1 лоджия'),
           ('2 лоджии', '2 лоджии'), )
    balcony = models.CharField(max_length=15, choices=bch, verbose_name='Балкон:', default='нет',)

    class Meta:
        verbose_name = 'Квартира'
        verbose_name_plural = 'Квартиры'

class House(RealtyEstate):
    number_of_floors_choises = (('1','1'),('2','2'),('3','3'),('4','4'),('5','5'),('6','6'))
    number_of_floors = models.CharField(max_length=1, verbose_name='Этажность:', choices=number_of_floors_choises,)

    number_of_flats_choises = (('1','1'),('2','2'),('3','3'),('4','4'),('5','5'),('6','6'),('7','7'),('8','8'),('9','9'),('10','10'),
                        ('11','11'),('12','12'),('13','13'),('14','14'),('15','15'),('16','16'),('17','17'),('18','18'),
                        ('19','19'),('20','20'),)
    number_of_flats = models.CharField(max_length=3, verbose_name='Комнат:', choices=number_of_flats_choises,)

    type_of_house_choises = (('Монолитный','Монолитный'), ('Блочный','Блочный'), ('Каркасно-монолитный','Каркасно-монолитный'),
                          ('Кирпичный','Кирпичный'), ('Деревянный','Деревянный'), ('Панельный','Панельный'),
                          ('Монолитно-кирпичный','Монолитно-кирпичный'))
    type_of_house = models.CharField(max_length=25, verbose_name='Тип дома', choices= type_of_house_choises,)

    plot_area = models.IntegerField(default='0',  verbose_name='Площадь участка (В МЕТРАХ!)')

    class Meta:
        verbose_name = 'Дом'
        verbose_name_plural = 'Дома'

class PlotOfLand(RealtyEstate):
    relief_choises = (('Ровный', 'Ровный'), ('Уклон', 'Уклон'))
    relief = models.CharField(verbose_name='Вид рельефа:', max_length=25, choices=relief_choises, )
    view_choises = (('На море', 'На море'), ('На горы', 'На горы'), ('На море и горы', 'На море и горы'))
    view = models.CharField(verbose_name='Вид', max_length=25, choices=view_choises)

    class Meta:
        verbose_name = 'Участок'
        verbose_name_plural = 'Участки'

class Commerce(RealtyEstate):
    type_of_building_choises = (('Торговое помещение', 'Торговое помещение'),
                             ('Помещение Свободного назначения', 'Помещение Свободного назначения'),
                             ('Склад', 'Склад'), ('Офисное помещение', 'Офисное помещение'),
                             ('Производство', 'Производство'),
                             ('Другая коммерческая недвижимость', 'Другая коммерческая недвижимость'),
                             )
    type_of_building = models.CharField(verbose_name='Тип строения', max_length=80, choices=type_of_building_choises,)
    type_deal_choises = (('аренда', 'аренда'), ('продажа', 'продажа'),)
    type_deal = models.CharField(verbose_name='Тип Сделки', max_length=80, choices=type_deal_choises,)

    class Meta:
        verbose_name = 'Коммерция'
        verbose_name_plural = 'Коммерция'

class Client(models.Model):
    creation_date = models.DateField(verbose_name='Дата создания', auto_now_add=True)
    author = models.ForeignKey('accounts.MyUser', verbose_name='Автор', related_name='client_author_id',
                               on_delete=models.CASCADE)
    status = models.BooleanField('Клиент закрыт', default=False)
    client_name = models.CharField(max_length=45,verbose_name='Клиент(ФИО)')
    phone = models.CharField('Телефон клиента', help_text='9881112233', max_length=10,)
    email = models.EmailField('email клиента', default='nomail@nomail.ru')
    estate_type = models.CharField(verbose_name='Что ищет', max_length=45, choices=RealtyEstate.type_choises)
    district = models.ManyToManyField(DistrictQuide, verbose_name='Район', related_name='client_distinkt_id',)
    discription = models.TextField('Примечание')
    min_price = models.IntegerField('Бюджет от:', validators=[MinValueValidator(300000)])
    max_price = models.IntegerField('Бюджет до:', validators=[MinValueValidator(300000)])

    def __str__(self):
        return self.client_name
    def clean(self):
        errors = {}
        if self.min_price is not None and self.max_price is not None:
            if (self.min_price >= self.max_price):
                errors['min_price'] = 'the min price is more than max price'
        if errors:
            raise ValidationError(errors)
    class Meta:
        verbose_name = ' Клиенты'
        verbose_name_plural = ' Клиенты'