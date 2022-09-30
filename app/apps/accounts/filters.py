import django_filters

from django_filters import ModelChoiceFilter
from django_select2.forms import ModelSelect2Widget

from app.apps.accounts.models import MyUser, Departament
from app.apps.real_estate.models import CityQuide


class UserListFilter(django_filters.FilterSet):
    department_boss = django_filters.BooleanFilter()
    is_active = django_filters.BooleanFilter()
    departament__city = ModelChoiceFilter(
        queryset=CityQuide.objects.all(),
        label="Город",
        widget=ModelSelect2Widget(
            search_fields=["name__icontains"],
            max_results=500,
            attrs={"data-minimum-input-length": 0},
        ),
    )

    departament = ModelChoiceFilter(
        queryset=Departament.objects.all(),
        label="Отдел",
        widget=ModelSelect2Widget(
            search_fields=["name__icontains"],
            dependent_fields={"departament__city": "city"},
            max_results=500,
            attrs={"data-minimum-input-length": 0},
        ),
    )

    class Meta:
        model = MyUser
        fields = {}
