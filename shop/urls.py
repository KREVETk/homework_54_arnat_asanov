from django.urls import path
from . import views

urlpatterns = [
    path('', views.products_view, name='products'),
    path('products/', views.products_view, name='products'),
    path('products/<int:pk>/', views.product_view, name='product_detail'),
    path('products/add/', views.product_add_view, name='product_add'),
    path('products/<int:pk>/edit/', views.product_edit_view, name='product_edit'),
    path('products/<int:pk>/delete/', views.product_delete_view, name='product_delete'),  # добавлен путь удаления
    path('categories/add/', views.category_add_view, name='category_add'),
    path('categories/<int:pk>/', views.category_detail_view, name='category_detail'),
    path('categories/<int:pk>/delete/', views.category_delete_view, name='category_delete'),
]

