from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Cart, CartItem, Book
from .serializers import CartSerializer, CartItemSerializer

class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(customer__user=self.request.user)

    def get_or_create_cart(self):
        cart = Cart.objects.filter(customer__user=self.request.user).first()
        if not cart:
            # Assuming you have a Customer model with OneToOne relation to User
            customer = self.request.user.customer
            cart = Cart.objects.create(customer=customer)
        return cart

    def list(self, request):
        # Get or create cart for current user
        cart = self.get_or_create_cart()
        serializer = self.get_serializer(cart)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def add_item(self, request):
        # Get or create cart for current user
        cart = self.get_or_create_cart()
        book_id = request.data.get('book_id')
        quantity = int(request.data.get('quantity', 1))

        try:
            book = Book.objects.get(id=book_id)
            cart_item = cart.add_item(book, quantity)
            serializer = CartItemSerializer(cart_item)
            return Response(serializer.data)
        except (Book.DoesNotExist, ValueError) as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(cart__customer__user=self.request.user)

    def perform_update(self, serializer):
        cart_item = self.get_object()
        quantity = self.request.data.get('quantity', cart_item.quantity)

        if quantity > cart_item.book.stock:
            raise serializers.ValidationError(
                {'quantity': f'Not enough stock. Available: {cart_item.book.stock}'}
            )

        serializer.save(quantity=quantity)