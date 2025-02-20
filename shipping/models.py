# shipping/models.py

from django.db import models

class ShippingMethod(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    estimated_days = models.PositiveIntegerField()  # Thời gian vận chuyển dự kiến
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'shipping'
        db_table = 'shipping_methods'

    def __str__(self):
        return f"{self.name} ({self.estimated_days} days)"

class ShippingAddress(models.Model):
    customer_id = models.IntegerField()
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'shipping'
        db_table = 'shipping_addresses'

    def __str__(self):
        return f"{self.full_name} - {self.city}"

class Shipment(models.Model):
    SHIPMENT_STATUS = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('in_transit', 'In Transit'),
        ('delivered', 'Delivered'),
        ('failed', 'Failed')
    )

    order_id = models.IntegerField()
    shipping_method = models.ForeignKey(ShippingMethod, on_delete=models.PROTECT)
    tracking_number = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20, choices=SHIPMENT_STATUS, default='pending')
    shipping_address = models.ForeignKey(ShippingAddress, on_delete=models.PROTECT)
    estimated_delivery_date = models.DateField()
    actual_delivery_date = models.DateField(null=True, blank=True)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'shipping'
        db_table = 'shipments'

    def __str__(self):
        return f"Shipment #{self.id} - Order #{self.order_id}"