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
        fields = ['name', 'description']


class ProductSearchForm(forms.Form):
    query = forms.CharField(required=False, label='Поиск по названию')
