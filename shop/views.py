from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
from .forms import ProductForm, CategoryForm

def products_view(request):
    products = Product.objects.all()
    return render(request, 'shop/products.html', {'products': products})

def product_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'shop/product_detail.html', {'product': product})

def product_add_view(request):
    form = ProductForm(request.POST or None)
    if form.is_valid():
        product = form.save()
        return redirect('product_detail', pk=product.pk)
    return render(request, 'shop/product_form.html', {'form': form})

def category_add_view(request):
    form = CategoryForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('products')
    return render(request, 'shop/category_form.html', {'form': form})

