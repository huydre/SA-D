from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from cart import views as cart_views

router = DefaultRouter()
router.register(r'books', views.BookViewSet, basename='book')
router.register(r'carts', cart_views.CartViewSet, basename='cart')
router.register(r'cart-items', cart_views.CartItemViewSet, basename='cart-item')

urlpatterns = [
    path('', include(router.urls)),
]