from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category
from .forms import CategoryForm, ProductForm


def products_view(request):
    query = request.GET.get('q')
    products = Product.objects.filter(stock__gte=1)
    if query:
        products = products.filter(name__icontains=query)
    products = products.order_by('category__name', 'name')

    categories = Category.objects.all().order_by('name')

    return render(request, 'shop/products_list.html', {
        'products': products,
        'query': query,
        'categories': categories,
        'selected_category': None,
    })


def products_by_category_view(request, category_name):
    query = request.GET.get('q')
    category = get_object_or_404(Category, name=category_name)
    products = Product.objects.filter(category=category, stock__gte=1)
    if query:
        products = products.filter(name__icontains=query)
    products = products.order_by('name')

    categories = Category.objects.all().order_by('name')

    return render(request, 'shop/products_list.html', {
        'products': products,
        'query': query,
        'categories': categories,
        'selected_category': category,
    })


def product_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'shop/product_detail.html', {'product': product})


def product_add_view(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()
            return redirect('product_detail', pk=product.pk)
    else:
        form = ProductForm()
    return render(request, 'shop/product_form.html', {'form': form})


def product_edit_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_detail', pk=product.pk)
    else:
        form = ProductForm(instance=product)
    return render(request, 'shop/product_form.html', {'form': form, 'product': product})


def product_delete_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('products')
    return render(request, 'shop/product_confirm_delete.html', {'product': product})


def category_add_view(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categories_list')
    else:
        form = CategoryForm()
    return render(request, 'shop/category_add.html', {'form': form})


def category_detail_view(request, pk):
    category = get_object_or_404(Category, pk=pk)
    return render(request, 'shop/category_detail.html', {'category': category})


def category_delete_view(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('categories_list')
    return render(request, 'shop/category_confirm_delete.html', {'category': category})


def categories_view(request):
    categories = Category.objects.all()
    return render(request, 'shop/categories_list.html', {'categories': categories})


def category_edit_view(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('categories_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'shop/category_edit.html', {'form': form, 'category': category})
