# shipping/serializers.py

from rest_framework import serializers
from .models import ShippingMethod, ShippingAddress, Shipment

class ShippingMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingMethod
        fields = '__all__'

class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = '__all__'

class ShipmentSerializer(serializers.ModelSerializer):
    shipping_method_details = ShippingMethodSerializer(source='shipping_method', read_only=True)
    shipping_address_details = ShippingAddressSerializer(source='shipping_address', read_only=True)

    class Meta:
        model = Shipment
        fields = ['id', 'order_id', 'shipping_method', 'shipping_method_details',
                 'tracking_number', 'status', 'shipping_address',
                 'shipping_address_details', 'estimated_delivery_date',
                 'actual_delivery_date', 'shipping_cost', 'notes',
                 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def create(self, validated_data):
        # Tạo tracking number
        import uuid
        validated_data['tracking_number'] = str(uuid.uuid4()).upper()[:12]
        return super().create(validated_data)