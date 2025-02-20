# order/serializers.py

from rest_framework import serializers
from .models import Order, OrderItem
from decimal import Decimal

class OrderItemSerializer(serializers.ModelSerializer):
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'book_id', 'book_title', 'quantity', 'price', 'subtotal']

    def create(self, validated_data):
        # Tính toán subtotal trước khi tạo OrderItem
        quantity = validated_data.get('quantity', 1)
        price = validated_data.get('price', Decimal('0.00'))
        validated_data['subtotal'] = quantity * price
        return super().create(validated_data)

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'customer_id', 'customer_email', 'customer_name',
                 'order_date', 'status', 'total_amount', 'shipping_address',
                 'payment_status', 'items', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        # Tạo order
        order = Order.objects.create(**validated_data)
        
        # Tạo order items
        for item_data in items_data:
            quantity = item_data.get('quantity', 1)
            price = item_data.get('price', Decimal('0.00'))
            OrderItem.objects.create(
                order=order,
                **item_data,
                subtotal=quantity * price
            )
            
        return order

    def validate(self, data):
        # Kiểm tra và tính toán total_amount nếu không được cung cấp
        if 'total_amount' not in data:
            total = sum(
                item['quantity'] * item['price']
                for item in data.get('items', [])
            )
            data['total_amount'] = total
        return data