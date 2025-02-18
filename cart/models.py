from django.db import models
from django.conf import settings
from decimal import Decimal

from book.models import Book
from customer.models import Customer

class Cart(models.Model):
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        verbose_name="Customer",
        related_name="carts"
    )
    created_at = models.DateTimeField("Created At", auto_now_add=True)
    updated_at = models.DateTimeField("Updated At", auto_now=True)
    status = models.CharField(
        "Status",
        max_length=20,
        choices=[
            ('active', 'Active'),
            ('completed', 'Completed'),
            ('abandoned', 'Abandoned')
        ],
        default='active'
    )

    class Meta:
        verbose_name = "Cart"
        verbose_name_plural = "Carts"
        ordering = ['-created_at']

    def __str__(self):
        return f"Cart {self.id} - {self.customer}"

    @property
    def total_amount(self):
        """Tính tổng giá trị giỏ hàng"""
        return sum(item.subtotal for item in self.items.all())

    @property
    def total_items(self):
        """Tính tổng số lượng sản phẩm trong giỏ hàng"""
        return sum(item.quantity for item in self.items.all())

    def add_item(self, book, quantity=1):
        """Thêm sách vào giỏ hàng"""
        if quantity <= 0:
            raise ValueError("Quantity must be positive")

        if quantity > book.stock:
            raise ValueError(f"Not enough stock. Available: {book.stock}")

        cart_item, created = CartItem.objects.get_or_create(
            cart=self,
            book=book,
            defaults={'quantity': quantity}
        )

        if not created:
            cart_item.quantity += quantity
            if cart_item.quantity > book.stock:
                raise ValueError(f"Not enough stock. Available: {book.stock}")
            cart_item.save()

        return cart_item

    def remove_item(self, book):
        """Xóa sách khỏi giỏ hàng"""
        self.items.filter(book=book).delete()

    def clear(self):
        """Xóa tất cả sản phẩm trong giỏ hàng"""
        self.items.all().delete()

class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        verbose_name="Cart",
        related_name="items"
    )
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        verbose_name="Book"
    )
    quantity = models.PositiveIntegerField("Quantity", default=1)
    price_at_time = models.DecimalField(
        "Price at Time",
        max_digits=10,
        decimal_places=2,
        help_text="Price of the book when added to cart"
    )
    created_at = models.DateTimeField("Created At", auto_now_add=True)
    updated_at = models.DateTimeField("Updated At", auto_now=True)

    class Meta:
        verbose_name = "Cart Item"
        verbose_name_plural = "Cart Items"
        unique_together = ('cart', 'book')
        ordering = ['created_at']

    def __str__(self):
        return f"{self.quantity} x {self.book.title} in Cart {self.cart.id}"

    def clean(self):
        """Validate the cart item"""
        from django.core.exceptions import ValidationError

        if self.quantity > self.book.stock:
            raise ValidationError({
                'quantity': f'Not enough stock. Available: {self.book.stock}'
            })

    def save(self, *args, **kwargs):
        """Override save to set price_at_time if not set"""
        if not self.price_at_time:
            self.price_at_time = self.book.price
        super().save(*args, **kwargs)

    @property
    def subtotal(self):
        """Tính tổng giá trị của item"""
        return Decimal(str(self.quantity)) * self.price_at_time