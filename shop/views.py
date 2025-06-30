from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category
from .forms import CategoryForm, ProductForm

def products_view(request):
    products = Product.objects.all()
    return render(request, 'shop/products_list.html', {'products': products})

def product_view(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'shop/product_detail.html', {'product': product})

def category_add_view(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categories_add')
    else:
        form = CategoryForm()
    return render(request, 'shop/category_add.html', {'form': form})

def product_add_view(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()
            return redirect('product_detail', id=product.id)
    else:
        form = ProductForm()
    return render(request, 'shop/product_add.html', {'form': form})
