from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404
from .models import Product, Category
from .forms import ProductForm



class ProductListView(ListView):
    model = Product
    template_name = 'shop/products_list.html'
    context_object_name = 'products'
    paginate_by = 5

    def get_queryset(self):
        queryset = Product.objects.filter(stock__gte=1).order_by('category__name', 'name')
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(name__icontains=query)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        context['categories'] = Category.objects.all().order_by('name')
        context['selected_category'] = None
        return context


class ProductsByCategoryView(ListView):
    model = Product
    template_name = 'shop/products_list.html'
    context_object_name = 'products'
    paginate_by = 5

    def get_queryset(self):
        slug = self.kwargs['slug']
        category = get_object_or_404(Category, slug=slug)
        queryset = Product.objects.filter(category=category, stock__gte=1).order_by('name')
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(name__icontains=query)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs['slug']
        category = get_object_or_404(Category, slug=slug)
        context['query'] = self.request.GET.get('q', '')
        context['categories'] = Category.objects.all().order_by('name')
        context['selected_category'] = category
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop/product_detail.html'
    context_object_name = 'product'


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'shop/product_form.html'

    def get_success_url(self):
        return reverse('product_detail', kwargs={'pk': self.object.pk})


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'shop/product_form.html'

    def get_success_url(self):
        return reverse('product_detail', kwargs={'pk': self.object.pk})


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'shop/product_confirm_delete.html'
    success_url = reverse_lazy('products')


class CategoryListView(ListView):
    model = Category
    template_name = 'shop/categories_list.html'
    context_object_name = 'categories'
    ordering = ['name']


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'shop/category_detail.html'
    context_object_name = 'category'


class CategoryCreateView(CreateView):
    model = Category
    fields = ['name', 'slug']
    template_name = 'shop/category_form.html'

    def get_success_url(self):
        return reverse('category_detail', kwargs={'pk': self.object.pk})


class CategoryUpdateView(UpdateView):
    model = Category
    fields = ['name', 'slug']
    template_name = 'shop/category_form.html'

    def get_success_url(self):
        return reverse('category_detail', kwargs={'pk': self.object.pk})


class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'shop/category_confirm_delete.html'
    success_url = reverse_lazy('categories_list')
