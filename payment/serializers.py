# payment/serializers.py

from rest_framework import serializers
from .models import PaymentMethod, Payment, Refund

class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer):
    payment_method_details = PaymentMethodSerializer(source='payment_method', read_only=True)

    class Meta:
        model = Payment
        fields = ['id', 'order_id', 'payment_method', 'payment_method_details',
                 'amount', 'status', 'transaction_id', 'payment_date',
                 'notes', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at', 'transaction_id']

    def create(self, validated_data):
        # Tạo transaction ID
        import uuid
        validated_data['transaction_id'] = f"PAY-{str(uuid.uuid4()).upper()[:8]}"
        return super().create(validated_data)

class RefundSerializer(serializers.ModelSerializer):
    payment_details = PaymentSerializer(source='payment', read_only=True)

    class Meta:
        model = Refund
        fields = ['id', 'payment', 'payment_details', 'amount', 'reason',
                 'status', 'refund_date', 'notes', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def validate_amount(self, value):
        payment = self.initial_data.get('payment')
        if payment and value > payment.amount:
            raise serializers.ValidationError("Refund amount cannot exceed payment amount")
        return value