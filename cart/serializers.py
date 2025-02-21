from project1.mongodb_client import get_db
from rest_framework import serializers
from .models import Cart, CartItem, Book
from bson import ObjectId
from bson.errors import InvalidId

class CartBookSerializer(serializers.Serializer):
    _id = serializers.CharField(source='book_id')
    title = serializers.CharField(read_only=True)
    author = serializers.CharField(read_only=True)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    image = serializers.CharField(required=False, read_only=True)
    stock = serializers.IntegerField(read_only=True)

class CartItemSerializer(serializers.ModelSerializer):
    book = CartBookSerializer(read_only=True)
    book_id = serializers.CharField(write_only=True)
    price_at_time = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'book', 'book_id', 'quantity', 'price_at_time', 'subtotal']
        read_only_fields = ['id', 'cart', 'price_at_time', 'subtotal']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        try:
            db = get_db()
            book_collection = db['books']
            book = book_collection.find_one({'_id': ObjectId(instance.book_id)})

            if book:
                data['book'] = {
                    '_id': str(book['_id']),
                    'title': book.get('title', ''),
                    'author': book.get('author', ''),
                    'price': str(book.get('price', 0)),
                    'image': book.get('image', ''),
                    'stock': book.get('stock', 0)
                }
            data['subtotal'] = str(instance.subtotal)

        except Exception as e:
            print(f"Error fetching book details: {e}")

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
        fields = ['id', 'customer_id', 'status', 'items', 'total_amount',
                 'total_items', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']