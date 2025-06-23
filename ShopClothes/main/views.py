from django.shortcuts import render
from django.views.generic import DetailView,ListView,CreateView,UpdateView,DeleteView

from cart.forms import CartAddProductForm
from .models import Product,Brand,Category
from django.db.models import Max

def home(request):
    return render(request,'main/home.html')



class ProductList(ListView):
    model = Product
    template_name = 'main/clothes_list.html'
    context_object_name = 'products'
    paginate_by = 8

    def get_queryset(self):
        queryset = super().get_queryset()
        # Получаем параметры из GET для фильтрации
        sizes = self.request.GET.getlist('size')
        brands = self.request.GET.getlist('brand')
        categories = self.request.GET.getlist('category')
        price_min = self.request.GET.get('price_min')
        price_max = self.request.GET.get('price_max')

        if sizes:
            queryset = queryset.filter(size__in=sizes)
        if brands:
            queryset = queryset.filter(brand__slug__in=brands)
        if categories:
            queryset = queryset.filter(category__slug__in=categories)
        if price_min:
            queryset = queryset.filter(price__gte=price_min)
        if price_max:
            queryset = queryset.filter(price__lte=price_max)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['brands'] = Brand.objects.all()
        context['categories'] = Category.objects.all()
        context['sizes'] = Product.SIZE_CHOICES

        # остальные переменные

        # Передаем выбранные фильтры обратно в контекст для сохранения состояния чекбоксов
        context['selected_sizes'] = self.request.GET.getlist('size')
        context['selected_brands'] = self.request.GET.getlist('brand')
        context['selected_categories'] = self.request.GET.getlist('category')
        context['price_min'] = self.request.GET.get('price_min', '')
        context['price_max'] = self.request.GET.get('price_max', '')

        context['max_price'] = Product.objects.aggregate(Max('price'))['price__max'] or 100000

        return context


class CategoryView(ListView):
    model=Product
    template_name='main/category.html'
    context_object_name='product'
    category=None

    def get_queryset(self):
        self.category = Category.objects.get(slug=self.kwargs['slug'])
        queryset = Product.objects.all().filter(category__slug=self.category.slug)
        return queryset
    
class BrandView(ListView):
    model=Product
    template_name='main/brand.html'
    context_object_name='product'
    brand=None

    def get_queryset(self):
        self.brand = Brand.objects.get(slug=self.kwargs['slug'])
        queryset = Product.objects.all().filter(brand__slug=self.brand.slug)
        return queryset
    
class ProductDetail(DetailView):
    model=Product
    context_object_name='product'
    template_name='main/clothes_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart_product_form'] = CartAddProductForm()
        return context