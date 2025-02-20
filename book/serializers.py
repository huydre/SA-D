# serializers.py
from rest_framework import serializers
from .models import Book
from bson import ObjectId
import logging
from datetime import datetime, date
from pymongo import MongoClient
from django.conf import settings

logger = logging.getLogger(__name__)

class BookSerializer(serializers.ModelSerializer):
    publication_date = serializers.DateField()
    image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Book
        fields = ['_id', 'title', 'author', 'description', 'price', 'stock',
                 'isbn', 'publisher', 'publication_date', 'image',
                 'created_at', 'updated_at']
        read_only_fields = ['_id', 'created_at', 'updated_at']

    def create(self, validated_data):
        try:
            logger.info(f"Starting book creation with data: {validated_data}")

            # Handle image upload
            image_file = validated_data.pop('image', None)
            image_path = None
            if image_file:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                file_name = f"books/{timestamp}_{image_file.name}"
                from django.core.files.storage import default_storage
                from django.core.files.base import ContentFile
                image_path = default_storage.save(file_name, ContentFile(image_file.read()))
                logger.info(f"Image saved at: {image_path}")

            # MongoDB connection
            client = MongoClient('mongodb://localhost:27017/')
            database = client['bookstore']
            collection = database['books']

            # Prepare book data
            book_data = {
                'title': validated_data.get('title'),
                'author': validated_data.get('author'),
                'description': validated_data.get('description'),
                'price': float(validated_data.get('price', 0)),
                'stock': int(validated_data.get('stock', 0)),
                'isbn': validated_data.get('isbn'),
                'publisher': validated_data.get('publisher'),
                'image': image_path,
                'created_at': datetime.now(),
                'updated_at': datetime.now()
            }

            # Handle publication date - store as date object
            pub_date = validated_data.get('publication_date')
            if pub_date:
                if isinstance(pub_date, str):
                    book_data['publication_date'] = datetime.strptime(pub_date, '%Y-%m-%d').date()
                elif isinstance(pub_date, date):
                    book_data['publication_date'] = pub_date
                elif isinstance(pub_date, datetime):
                    book_data['publication_date'] = pub_date.date()

            logger.info(f"Attempting to insert book data: {book_data}")

            result = collection.insert_one(book_data)
            if not result.inserted_id:
                if image_path:
                    default_storage.delete(image_path)
                raise serializers.ValidationError("Failed to insert book into database")

            created_book = collection.find_one({'_id': result.inserted_id})
            if not created_book:
                if image_path:
                    default_storage.delete(image_path)
                raise serializers.ValidationError("Could not retrieve created book")

            book = Book()
            created_book['_id'] = str(created_book['_id'])

            for key, value in created_book.items():
                if hasattr(book, key):
                    if key == 'publication_date' and value:
                        if isinstance(value, datetime):
                            value = value.date()
                    setattr(book, key, value)

            return book

        except Exception as e:
            if 'image_path' in locals() and image_path:
                default_storage.delete(image_path)
            logger.error(f"Error creating book: {str(e)}", exc_info=True)
            raise serializers.ValidationError(f"Error creating book: {str(e)}")


    def to_representation(self, instance):
        data = super().to_representation(instance)
        if '_id' in data and data['_id']:
            data['_id'] = str(data['_id'])
        
        for field in ['publication_date', 'created_at', 'updated_at']:
            if field in data and data[field]:
                if isinstance(data[field], (datetime, date)):
                    data[field] = data[field].isoformat()
                
        return data

    def validate(self, data):
        logger.info(f"Validating data: {data}")
        
        required_fields = ['title', 'author', 'price', 'stock', 'isbn']
        for field in required_fields:
            if field not in data:
                raise serializers.ValidationError(f"{field} is required")

        if 'price' in data:
            try:
                price = float(data['price'])
                if price <= 0:
                    raise serializers.ValidationError("Price must be greater than 0")
                data['price'] = price
            except (TypeError, ValueError):
                raise serializers.ValidationError("Invalid price format")

        if 'stock' in data:
            try:
                stock = int(data['stock'])
                if stock < 0:
                    raise serializers.ValidationError("Stock cannot be negative")
                data['stock'] = stock
            except (TypeError, ValueError):
                raise serializers.ValidationError("Invalid stock format")

        if 'publication_date' in data and data['publication_date']:
            if not isinstance(data['publication_date'], (date, str)):
                raise serializers.ValidationError("Invalid publication date format")

        return data