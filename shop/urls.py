from django.urls import path
from .views import (
    ProductListView, ProductDetailView, ProductCreateView, ProductUpdateView, ProductDeleteView, ProductsByCategoryView,
    CategoryListView, CategoryDetailView, CategoryCreateView, CategoryUpdateView, CategoryDeleteView,
    AddToCartView, CartView, RemoveFromCartView,)

urlpatterns = [
    path('', ProductListView.as_view(), name='products'),
    path('products/', ProductListView.as_view(), name='products'),
    path('products/category/<slug:slug>/', ProductsByCategoryView.as_view(), name='products_by_category'),
    path('products/add/', ProductCreateView.as_view(), name='product_add'),
    path('products/<int:pk>/edit/', ProductUpdateView.as_view(), name='product_edit'),
    path('products/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),

    path('categories/', CategoryListView.as_view(), name='categories_list'),
    path('categories/add/', CategoryCreateView.as_view(), name='category_add'),
    path('categories/<int:pk>/edit/', CategoryUpdateView.as_view(), name='category_edit'),
    path('categories/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category_delete'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category_detail'),

    path('cart/', CartView.as_view(), name='cart'),
    path('cart/add/<int:pk>/', AddToCartView.as_view(), name='add_to_cart'),
    path('cart/remove/<int:pk>/', RemoveFromCartView.as_view(), name='remove_from_cart'),
]