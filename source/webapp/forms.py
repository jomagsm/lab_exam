from django import forms

from webapp.models import CATEGORY_CHOICE, DEFAUL_CATEGORY


class ProductForm(forms.Form):
    name = forms.CharField(max_length=100, required=True, label='Название')
    description = forms.CharField(max_length=2000, required=False, label='Описание', widget=forms.Textarea)
    category = forms.ChoiceField(choices=CATEGORY_CHOICE, required=True, initial=DEFAUL_CATEGORY, label='Категория')
    amount = forms.IntegerField(min_value=0, required=True,label='Остаток')
    price = forms.DecimalField(min_value=0, max_digits=7, decimal_places=2, required=True, label='Цена')