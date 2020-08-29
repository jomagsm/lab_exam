from django import forms

from webapp.models import CATEGORY_CHOICE, DEFAUL_CATEGORY, Product, Basket, Order


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['name', 'description', 'category', 'amount', 'price']


class BasketForm(forms.Form):
    qty = forms.IntegerField(min_value= 0, required=True, label="", widget=forms.NumberInput(attrs={'class':'form-control  mt-3 mr-sm-2'}))


class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ['name', 'address', 'phone']


class ProfileSearchForm(forms.Form):
    name = forms.CharField(required=False)