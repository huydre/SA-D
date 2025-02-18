from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'description', 'price', 'stock',
                 'isbn', 'publisher', 'publication_date', 'image', 'image_url',
                 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
        return None

    def validate_isbn(self, value):
        # Loại bỏ dấu gạch ngang
        isbn = value.replace('-', '')

        if len(isbn) != 13:
            raise serializers.ValidationError('ISBN must be 13 digits')

        if not isbn.isdigit():
            raise serializers.ValidationError('ISBN must contain only digits')

        if not (isbn.startswith('978') or isbn.startswith('979')):
            raise serializers.ValidationError('ISBN must start with 978 or 979')

        return isbn

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError('Price must be greater than 0')
        return value

    def validate_stock(self, value):
        if value < 0:
            raise serializers.ValidationError('Stock cannot be negative')
        return value