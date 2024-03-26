from django.urls import path
from .import views


urlpatterns = [
    path("", views.index, name="index"),
    path("cart", views.cart, name="cart"),
    path("add_to_cart", views.add_to_cart, name="add"),
    path("decrement_to_cart", views.decrement_to_cart, name="decrement"),
    path("clear_cart", views.clear_cart, name="clear_cart"),
    path("confirm_payment/<str:pk>", views.confirm_payment, name="add")
]
