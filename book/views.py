from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Book
from .serializers import BookSerializer
import logging
from django.core.files.storage import default_storage
from datetime import datetime

logger = logging.getLogger(__name__)

class BookViewSet(viewsets.ModelViewSet):
    serializer_class = BookSerializer
    parser_classes = (MultiPartParser, FormParser)

    def get_queryset(self):
        try:
            return Book.objects.all().using('mongodb')
        except Exception as e:
            logger.error(f"Error getting queryset: {e}")
            return Book.objects.none()

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            logger.info(f"Initial queryset count: {queryset.count()}")

            books_data = []
            for book in queryset:
                try:
                    logger.info(f"Serializing book: {book.title}")
                    serializer = self.get_serializer(book)
                    book_data = serializer.data
                    books_data.append(book_data)
                except Exception as e:
                    logger.error(f"Error serializing book {getattr(book, '_id', 'unknown')}: {e}")
                    continue

            books_data = sorted(books_data, key=lambda x: x['title'])

            logger.info(f"Successfully serialized {len(books_data)} books")
            return Response({
                'count': len(books_data),
                'results': books_data
            })

        except Exception as e:
            logger.error(f"Error in list view: {e}", exc_info=True)
            return Response(
                {
                    "error": "Failed to fetch books",
                    "detail": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def create(self, request, *args, **kwargs):
        try:
            logger.info(f"Received data: {request.data}")
            logger.info(f"Received files: {request.FILES}")

            # Validate required fields
            required_fields = ['title', 'author', 'price', 'stock', 'isbn']
            for field in required_fields:
                if field not in request.data:
                    return Response(
                        {'error': f'{field} is required'},
                        status=status.HTTP_400_BAD_REQUEST
                    )

            # Create serializer with data
            serializer = self.get_serializer(data=request.data)

            if not serializer.is_valid():
                logger.error(f"Serializer errors: {serializer.errors}")
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            try:
                book = serializer.save()
                return Response(
                    self.get_serializer(book).data,
                    status=status.HTTP_201_CREATED
                )
            except Exception as save_error:
                logger.error(f"Error saving book: {save_error}")
                return Response(
                    {'error': str(save_error)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        except Exception as e:
            logger.error(f"Error in create view: {e}", exc_info=True)
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            old_image = instance.image if instance.image else None

            data = request.data.copy()
            
            # Handle image upload for updates
            if 'image' in request.FILES:
                image_file = request.FILES['image']
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"books/{timestamp}_{image_file.name}"
                file_path = default_storage.save(filename, image_file)
                data['image'] = file_path

            serializer = self.get_serializer(instance, data=data, partial=True)
            if not serializer.is_valid():
                # If new image was saved but validation failed, delete it
                if 'image' in data and default_storage.exists(data['image']):
                    default_storage.delete(data['image'])
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            # Save the updated instance
            book = serializer.save()

            # Delete old image if it was replaced
            if old_image and 'image' in data and old_image != data['image']:
                if default_storage.exists(old_image):
                    default_storage.delete(old_image)

            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error updating book: {e}")
            # Clean up new image if it was saved
            if 'data' in locals() and 'image' in data and default_storage.exists(data['image']):
                default_storage.delete(data['image'])
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            # Delete associated image if it exists
            if instance.image and default_storage.exists(instance.image):
                default_storage.delete(instance.image)
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            logger.error(f"Error deleting book: {e}")
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )