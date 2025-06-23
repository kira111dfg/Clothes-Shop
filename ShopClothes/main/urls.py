from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('products/',views.ProductList.as_view(),name='products'),
    path('product/<int:pk>',views.ProductDetail.as_view(),name='product'),
    path('category/<slug:slug>',views.CategoryView.as_view(),name='category'),
    path('brand/<slug:slug>',views.BrandView.as_view(),name='brand'),
    ]