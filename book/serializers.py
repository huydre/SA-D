from rest_framework import serializers
from .models import Book
from bson import ObjectId
import logging
from datetime import datetime, date
from pymongo import MongoClient
from django.conf import settings

logger = logging.getLogger(__name__)

class BookSerializer(serializers.ModelSerializer):
    publication_date = serializers.DateField(format='%Y-%m-%d')
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

            # Convert publication_date to string
            pub_date = validated_data.get('publication_date')
            pub_date_str = None
            if pub_date:
                if isinstance(pub_date, (date, datetime)):
                    pub_date_str = pub_date.strftime('%Y-%m-%d')
                elif isinstance(pub_date, str):
                    # Validate date string format
                    try:
                        datetime.strptime(pub_date, '%Y-%m-%d')
                        pub_date_str = pub_date
                    except ValueError:
                        raise serializers.ValidationError("Invalid date format. Use YYYY-MM-DD")

            # Prepare book data
            book_data = {
                'title': validated_data.get('title'),
                'author': validated_data.get('author'),
                'description': validated_data.get('description'),
                'price': float(validated_data.get('price', 0)),
                'stock': int(validated_data.get('stock', 0)),
                'isbn': validated_data.get('isbn'),
                'publisher': validated_data.get('publisher'),
                'publication_date': pub_date_str,
                'image': image_path,
                'created_at': datetime.now(),
                'updated_at': datetime.now()
            }

            logger.info(f"Attempting to insert book data: {book_data}")

            result = collection.insert_one(book_data)
            if not result.inserted_id:
                if image_path:
                    default_storage.delete(image_path)
                raise serializers.ValidationError("Failed to insert book into database")

            # Retrieve the created book
            created_book = collection.find_one({'_id': result.inserted_id})
            if not created_book:
                if image_path:
                    default_storage.delete(image_path)
                raise serializers.ValidationError("Could not retrieve created book")

            # Convert MongoDB document to Book instance
            book = Book()
            created_book['_id'] = str(created_book['_id'])

            for key, value in created_book.items():
                if hasattr(book, key):
                    if key == 'publication_date' and value:
                        try:
                            value = datetime.strptime(value, '%Y-%m-%d').date()
                        except (ValueError, TypeError):
                            value = None
                    setattr(book, key, value)

            return book

        except Exception as e:
            if 'image_path' in locals() and image_path:
                default_storage.delete(image_path)
            logger.error(f"Error creating book: {str(e)}", exc_info=True)
            raise serializers.ValidationError(f"Error creating book: {str(e)}")

    def to_representation(self, instance):
        data = super().to_representation(instance)

        # Convert ObjectId to string
        if '_id' in data and data['_id']:
            data['_id'] = str(data['_id'])

        # Convert dates to ISO format
        if 'publication_date' in data and data['publication_date']:
            if isinstance(data['publication_date'], (date, datetime)):
                data['publication_date'] = data['publication_date'].strftime('%Y-%m-%d')
            elif isinstance(data['publication_date'], str):
                try:
                    date_obj = datetime.strptime(data['publication_date'], '%Y-%m-%d')
                    data['publication_date'] = date_obj.strftime('%Y-%m-%d')
                except ValueError:
                    data['publication_date'] = None

        return data

    def validate(self, data):
        logger.info(f"Validating data: {data}")

        # Validate required fields
        required_fields = ['title', 'author', 'price', 'stock', 'isbn']
        for field in required_fields:
            if field not in data:
                raise serializers.ValidationError(f"{field} is required")

        # Validate price
        if 'price' in data:
            try:
                price = float(data['price'])
                if price <= 0:
                    raise serializers.ValidationError("Price must be greater than 0")
                data['price'] = price
            except (TypeError, ValueError):
                raise serializers.ValidationError("Invalid price format")

        # Validate stock
        if 'stock' in data:
            try:
                stock = int(data['stock'])
                if stock < 0:
                    raise serializers.ValidationError("Stock cannot be negative")
                data['stock'] = stock
            except (TypeError, ValueError):
                raise serializers.ValidationError("Invalid stock format")

        # Validate publication date
        if 'publication_date' in data and data['publication_date']:
            if isinstance(data['publication_date'], str):
                try:
                    datetime.strptime(data['publication_date'], '%Y-%m-%d')
                except ValueError:
                    raise serializers.ValidationError("Invalid publication date format. Use YYYY-MM-DD")

        return data
    
    