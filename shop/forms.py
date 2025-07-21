from django import forms
from .models import Product, Category


class ProductForm(forms.ModelForm):
    stock = forms.IntegerField(min_value=0, label='Остаток')
    price = forms.DecimalField(max_digits=7, decimal_places=2, label='Цена')

    class Meta:
        model = Product
        fields = ['name', 'description', 'category', 'price', 'stock', 'image']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description', 'slug']


class ProductSearchForm(forms.Form):
    query = forms.CharField(required=False, label='Поиск по названию')


class AddToCartForm(forms.Form):
    product_id = forms.IntegerField(widget=forms.HiddenInput)
    quantity = forms.IntegerField(min_value=1, label='Количество')


class OrderForm(forms.Form):
    username = forms.CharField(max_length=150, label='Имя', required=True)
    phone = forms.CharField(max_length=30, label='Телефон', required=True)
    address = forms.CharField(max_length=500, label='Адрес', required=True, widget=forms.Textarea(attrs={'rows': 2}))
