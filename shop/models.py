from django.db import models
from django.utils.text import slugify
from django.core.exceptions import ValidationError


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=300)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    created_at = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    stock = models.IntegerField(default=0)
    image = models.CharField(max_length=1000, blank=True)

    def clean(self):
        if self.stock < 0:
            raise ValidationError({'stock': 'Остаток не может быть меньше 0'})

    def __str__(self):
        return self.name


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.PositiveIntegerField(default=1)
    session_key = models.CharField(max_length=40)

    def clean(self):
        if self.quantity < 1:
            raise ValidationError('Количество товара в корзине должно быть не менее 1')
        if self.quantity > self.product.stock:
            raise ValidationError('Количество товара не может превышать остаток на складе')

    def subtotal(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f'{self.product.name} — {self.quantity} шт.'
