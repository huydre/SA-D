# payment/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PaymentMethodViewSet, PaymentViewSet, RefundViewSet

router = DefaultRouter()
router.register(r'methods', PaymentMethodViewSet)
router.register(r'payments', PaymentViewSet)
router.register(r'refunds', RefundViewSet)

urlpatterns = [
    path('', include(router.urls)),
]