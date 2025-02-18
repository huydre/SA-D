from rest_framework import viewsets, filters, status, parsers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from .models import Book
from .serializers import BookSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['author', 'price']
    search_fields = ['title', 'author']
    ordering_fields = ['price', 'created_at', 'title']
    ordering = ['title']

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        # AllowAny
        return [AllowAny()]

    def create(self, request, *args, **kwargs):
        # Get the image file from request
        image = request.FILES.get('image')

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Save the instance
        instance = serializer.save()

        # Handle image upload if present
        if image:
            instance.image = image
            instance.save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        # Get the image file from request
        image = request.FILES.get('image')

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        # Save the instance
        instance = serializer.save()

        # Handle image upload if present
        if image:
            # Delete old image if it exists
            if instance.image:
                instance.image.delete(save=False)
            instance.image = image
            instance.save()

        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def update_stock(self, request, pk=None):
        book = self.get_object()
        stock = request.data.get('stock', None)

        if stock is None:
            return Response(
                {'error': 'Stock value is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            stock = int(stock)
            if stock < 0:
                raise ValueError("Stock cannot be negative")

            book.stock = stock
            book.save()

            serializer = self.get_serializer(book)
            return Response(serializer.data)

        except ValueError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=['get'])
    def in_stock(self, request):
        books = Book.objects.filter(stock__gt=0)
        serializer = self.get_serializer(books, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def out_of_stock(self, request):
        books = Book.objects.filter(stock=0)
        serializer = self.get_serializer(books, many=True)
        return Response(serializer.data)
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)