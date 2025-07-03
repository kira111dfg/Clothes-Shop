from django.shortcuts import redirect, render
from django.views.generic import DetailView,ListView,CreateView,UpdateView,DeleteView

from .documents import ProductDocument

from .forms import CommentForm
from cart.forms import CartAddProductForm
from .models import Product,Brand,Category
from django.db.models import Max
from django.db.models import Case, When
from .documents import ProductDocument
from .models import Product
from django.shortcuts import render

def home(request):
    products=Product.objects.order_by('-id')[:6]
    brands=Brand.objects.order_by('-id')[:5]
    return render(request,'main/home.html',{'products':products,'brands':brands})



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
        price_min = self.request.GET.get('price_min', '').replace(' ', '')
        price_max = self.request.GET.get('price_max', '').replace(' ', '')
        
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
    context_object_name='products'
    category=None

    def get_queryset(self):
        self.category = Category.objects.get(slug=self.kwargs['slug'])
        queryset = Product.objects.all().filter(category__slug=self.category.slug)
        return queryset
    
class BrandView(ListView):
    model=Product
    template_name='main/brand.html'
    context_object_name='products'
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
        product = self.get_object()
        context['comments'] = product.comments.filter(active=True).order_by('-created')[:3]  # первые 3 активных комментария
        context['form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.product = self.object
            comment.save()
            return redirect(self.request.path)
        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)



def search_products(request):
    q = request.GET.get('q')
    products = []
    if q:
        search_results = ProductDocument.search()\
            .query("multi_match", query=q, fields=['title', 'description', 'brand.title'], fuzziness="AUTO")\
            .execute()
        ids = [int(hit.meta.id) for hit in search_results.hits]
        if ids:
            preserved_order = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(ids)])
            products = Product.objects.filter(id__in=ids).order_by(preserved_order)
    return render(request, 'main/search_results.html', {'results': products, 'query': q})
