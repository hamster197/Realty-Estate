
from django import forms
from django.forms import BaseInlineFormSet

from django.forms import inlineformset_factory
from django_select2.forms import ModelSelect2Widget

from app.apps.deals.models import Deal, RealtorInTheDeal, SubmittedCommission
from app.apps.real_estate.models import CityQuide, DistrictQuide


class DealEditForm(forms.ModelForm):
    city = forms.ModelChoiceField(
        queryset=CityQuide.objects.all(),
        label="Город",
        widget=ModelSelect2Widget(
            search_fields=["name__icontains"],
            max_results=500,
            attrs={"data-minimum-input-length": 0},
        ),
    )

    district = forms.ModelChoiceField(
        queryset=DistrictQuide.objects.all(),
        label="Район",
        widget=ModelSelect2Widget(
            search_fields=["name__icontains"],
            dependent_fields={"city": "city"},
            max_results=500,
            attrs={"data-minimum-input-length": 0},
        ),
    )
    class Meta:
        model = Deal
        fields = '__all__'

class BaseRealtorFormSet(BaseInlineFormSet):
    def clean(self):
        total_percentage = 0
        for form in self.forms:
            data = form.cleaned_data
            if data.get('percent') != None:
                total_percentage += data.get('percent')
        if total_percentage != 100:
            raise forms.ValidationError('Сумма процентов != 100 !')

DealFormset = inlineformset_factory(
    Deal,
    RealtorInTheDeal,
    exclude=('deal', 'realtor_commision_sum'),
    extra=1,
    formset=BaseRealtorFormSet,
)

class BaseCommisionFormSet(BaseInlineFormSet):
    def clean(self):
        total_sum = 0
        for form in self.forms:
            data = form.cleaned_data
            if data.get('deal') != None:
                deal = data.get('deal')
            if data.get('commission_sum') != None:
                total_sum += data.get('commission_sum')
        if self.forms:
            if total_sum > deal.commission:
                raise forms.ValidationError('Внесенная суммма коммисии больше внесенной в сделку !')

DealCommissionFormset = inlineformset_factory(
    Deal,
    SubmittedCommission,
    exclude=('deal', ),
    extra=1,
    formset=BaseCommisionFormSet,
)