

from django.urls import path, re_path, register_converter
from . import views
from . import converters
from .views import ProductsHome, RegisterUser, LoginUser

register_converter(converters.FourDigitYearConverter, "year4")

urlpatterns = [
    path('', views.index, name='home'),  # http://127.0.0.1:8000
    path('about/', ProductsHome.as_view(), name='about'),
    path('addpage/', views.addpage, name='add_page'),
    path('contact/', views.contact, name='contact'),
    path('logout/', views.logout_user, name='logout'),
    path('login/', LoginUser.as_view(), name='login'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('post/<slug:post_slug>/', views.show_post, name='post'),
    path('category/<slug:cat_slug>/', views.show_category, name='category'),
]
