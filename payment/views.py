# payment/views.py

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import PaymentMethod, Payment, Refund
from .serializers import PaymentMethodSerializer, PaymentSerializer, RefundSerializer

class PaymentMethodViewSet(viewsets.ModelViewSet):
    queryset = PaymentMethod.objects.all()
    serializer_class = PaymentMethodSerializer

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def get_queryset(self):
        queryset = Payment.objects.all()
        order_id = self.request.query_params.get('order_id')
        if order_id:
            queryset = queryset.filter(order_id=order_id)
        return queryset

    @action(detail=True, methods=['post'])
    def process_payment(self, request, pk=None):
        payment = self.get_object()
        # Thêm logic xử lý thanh toán ở đây
        payment.status = 'completed'
        payment.save()
        return Response({'status': 'payment processed'})

class RefundViewSet(viewsets.ModelViewSet):
    queryset = Refund.objects.all()
    serializer_class = RefundSerializer

    @action(detail=True, methods=['post'])
    def process_refund(self, request, pk=None):
        refund = self.get_object()
        # Thêm logic xử lý hoàn tiền ở đây
        refund.status = 'completed'
        refund.save()

        # Cập nhật trạng thái payment
        payment = refund.payment
        payment.status = 'refunded'
        payment.save()

        return Response({'status': 'refund processed'})