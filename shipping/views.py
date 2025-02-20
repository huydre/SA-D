# shipping/views.py

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import ShippingMethod, ShippingAddress, Shipment
from .serializers import ShippingMethodSerializer, ShippingAddressSerializer, ShipmentSerializer

class ShippingMethodViewSet(viewsets.ModelViewSet):
    queryset = ShippingMethod.objects.all()
    serializer_class = ShippingMethodSerializer

class ShippingAddressViewSet(viewsets.ModelViewSet):
    serializer_class = ShippingAddressSerializer

    def get_queryset(self):
        return ShippingAddress.objects.filter(
            customer_id=self.request.query_params.get('customer_id')
        )

    @action(detail=False, methods=['get'])
    def default_address(self, request):
        customer_id = request.query_params.get('customer_id')
        try:
            address = ShippingAddress.objects.get(
                customer_id=customer_id,
                is_default=True
            )
            serializer = self.get_serializer(address)
            return Response(serializer.data)
        except ShippingAddress.DoesNotExist:
            return Response(
                {"detail": "No default address found"},
                status=status.HTTP_404_NOT_FOUND
            )

class ShipmentViewSet(viewsets.ModelViewSet):
    queryset = Shipment.objects.all()
    serializer_class = ShipmentSerializer

    def get_queryset(self):
        queryset = Shipment.objects.all()
        order_id = self.request.query_params.get('order_id')
        if order_id:
            queryset = queryset.filter(order_id=order_id)
        return queryset

    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        shipment = self.get_object()
        new_status = request.data.get('status')
        if new_status in dict(Shipment.SHIPMENT_STATUS):
            shipment.status = new_status
            shipment.save()
            return Response({'status': 'status updated'})
        return Response(
            {'error': 'Invalid status'},
            status=status.HTTP_400_BAD_REQUEST
        )