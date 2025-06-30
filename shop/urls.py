from django.urls import path
from . import views

urlpatterns = [
    path('', views.products_view, name='products'),
    path('products/', views.products_view, name='products'),
    path('products/<int:pk>/', views.product_view, name='product_detail'),
    path('products/add/', views.product_add_view, name='product_add'),
    path('categories/add/', views.category_add_view, name='category_add'),
]
