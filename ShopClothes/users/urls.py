from django.urls import path,include
from . import views
from django.contrib.auth.views import LogoutView



app_name='users'

urlpatterns = [
    path('login/', views.MyLogin.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='users:login'), name='logout'),
    path('register/',views.register,name='register')
]