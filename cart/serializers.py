from project1.mongodb_client import get_db
from rest_framework import serializers
from .models import Cart, CartItem, Book
from bson import ObjectId
from bson.errors import InvalidId

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'price', 'stock']

class CartItemSerializer(serializers.ModelSerializer):
    book_id = serializers.CharField()
    price_at_time = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'book_id', 'quantity', 'price_at_time', 'subtotal']
        read_only_fields = ['id', 'cart', 'price_at_time', 'subtotal']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['subtotal'] = str(instance.subtotal)
        return data

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be positive")
        return value
    
    def validate_book_id(self, value):
        try:
            book_id = ObjectId(value)
            db = get_db()
            book_collection = db['books']
            book = book_collection.find_one({'_id': book_id})

            if not book:
                raise serializers.ValidationError("Book does not exist")
            return value
        except InvalidId:
            raise serializers.ValidationError("Invalid book ID format")

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_amount = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True
    )
    total_items = serializers.IntegerField(read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'customer', 'status', 'items', 'total_amount',
                 'total_items', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']