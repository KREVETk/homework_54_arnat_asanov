from django.core.exceptions import ValidationError
from django.db import transaction
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponseBadRequest
from .models import Product, Category, CartItem, Order, OrderItem
from .forms import ProductForm, OrderForm


class CategoryContextMixin:
    def get_category_context(self):
        return {
            'query': self.request.GET.get('q', ''),
            'categories': Category.objects.all().order_by('name'),
        }


def get_or_create_session_key(request):
    if not request.session.session_key:
        request.session.create()
    return request.session.session_key


def get_filtered_products(queryset, request):
    query = request.GET.get('q')
    if query:
        queryset = queryset.filter(name__icontains=query)
    return queryset


class ProductListView(CategoryContextMixin, ListView):
    model = Product
    template_name = 'shop/products_list.html'
    context_object_name = 'products'
    paginate_by = 5

    def get_queryset(self):
        queryset = Product.objects.filter(stock__gte=1).order_by('category__name', 'name')
        return get_filtered_products(queryset, self.request)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_category_context())
        context['selected_category'] = None
        return context


class ProductsByCategoryView(CategoryContextMixin, ListView):
    model = Product
    template_name = 'shop/products_list.html'
    context_object_name = 'products'
    paginate_by = 5

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        queryset = Product.objects.filter(category=self.category, stock__gte=1).order_by('name')
        return get_filtered_products(queryset, self.request)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_category_context())
        context['selected_category'] = self.category
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


class AddToCartView(View):
    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        quantity = request.POST.get('quantity')
        try:
            quantity = int(quantity)
            if quantity < 1:
                return HttpResponseBadRequest("Количество должно быть больше 0")
        except (ValueError, TypeError):
            return HttpResponseBadRequest("Некорректное количество")

        session_key = get_or_create_session_key(request)

        cart_item, _ = CartItem.objects.get_or_create(
            product=product,
            session_key=session_key,
            defaults={'quantity': 0}
        )

        new_quantity = cart_item.quantity + quantity
        if new_quantity > product.stock:
            cart_item.quantity = product.stock
        else:
            cart_item.quantity = new_quantity

        try:
            cart_item.full_clean()
            cart_item.save()
        except ValidationError as e:
            return HttpResponseBadRequest(e.messages)

        return redirect(request.META.get('HTTP_REFERER', reverse('products')))


class RemoveFromCartView(View):
    def post(self, request, pk):
        session_key = get_or_create_session_key(request)
        cart_item = get_object_or_404(CartItem, pk=pk, session_key=session_key)

        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            try:
                cart_item.full_clean()
                cart_item.save()
            except ValidationError as e:
                return HttpResponseBadRequest(e.messages)
        else:
            cart_item.delete()

        return redirect('cart')


class CartView(View):
    def get(self, request):
        session_key = get_or_create_session_key(request)
        cart_items = CartItem.objects.filter(session_key=session_key).select_related('product')
        total = sum(item.subtotal() for item in cart_items)
        return render(request, 'shop/cart.html', {
            'cart_items': cart_items,
            'total': total,
            'order_form': OrderForm(),
        })


class OrderCreateView(View):
    @transaction.atomic
    def post(self, request):
        session_key = get_or_create_session_key(request)
        cart_items = CartItem.objects.filter(session_key=session_key).select_related('product')

        if not cart_items.exists():
            return redirect('cart')

        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart_items:
                OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)
                item.product.stock -= item.quantity
                item.product.save()
            cart_items.delete()
            return redirect('products')
        else:
            total = sum(item.subtotal() for item in cart_items)
            return render(request, 'shop/cart.html', {
                'cart_items': cart_items,
                'total': total,
                'order_form': form,
            })
