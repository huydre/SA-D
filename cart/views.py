from jsonschema import ValidationError
from customer.models import Customer
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Cart, CartItem, Book
from .serializers import CartSerializer, CartItemSerializer
from bson import ObjectId
from project1.mongodb_client import get_db
from decimal import Decimal

class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        try:
            customer = Customer.objects.using('mysql').get(user_id=self.request.user.id)
            return Cart.objects.filter(customer_id=customer.id)
        except Customer.DoesNotExist:
            return Cart.objects.none()

    def get_or_create_cart(self):
        try:
            # Thêm logging để debug
            print(f"Finding customer for user: {self.request.user.id}")

            # Kiểm tra xem user có customer profile chưa
            customer = Customer.objects.using('mysql').get(user_id=self.request.user.id)

            print(f"Found customer: {customer.id}")

            # Tìm cart đang active của customer
            cart = Cart.objects.filter(
                customer_id=customer.id,
                status='active'
            ).first()

            # Nếu không có cart thì tạo mới
            if not cart:
                print(f"Creating new cart for customer: {customer.id}")
                cart = Cart.objects.create(
                    customer_id=customer.id,
                    status='active'
                )
            return cart

        except Customer.DoesNotExist:
            print(f"No customer found for user: {self.request.user.id}")
            # Tạo customer mới nếu chưa có
            customer = Customer.objects.using('mysql').create(
                user_id=self.request.user.id,
                # Thêm các trường bắt buộc khác của Customer model
            )

            # Tạo cart mới cho customer
            cart = Cart.objects.create(
                customer_id=customer.id,
                status='active'
            )
            return cart
        except Exception as e:
            print(f"Error in get_or_create_cart: {str(e)}")
            raise ValidationError(f"Error creating cart: {str(e)}")

    def list(self, request):
        cart = self.get_or_create_cart()

        # Prefetch related items
        cart = Cart.objects.prefetch_related('items').get(id=cart.id)

        serializer = self.get_serializer(cart)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def add_item(self, request):
        cart = self.get_or_create_cart()
        serializer = CartItemSerializer(data=request.data)

        if serializer.is_valid():
            try:
                # Lấy book từ MongoDB
                db = get_db()
                book_collection = db['books']
                book_id = ObjectId(serializer.validated_data['book_id'])
                book = book_collection.find_one({'_id': book_id})

                if not book:
                    return Response(
                        {'error': 'Book not found'},
                        status=status.HTTP_404_NOT_FOUND
                    )

                # Kiểm tra xem sách đã có trong giỏ hàng chưa
                existing_item = CartItem.objects.filter(
                    cart=cart,
                    book_id=str(book_id)
                ).first()

                new_quantity = serializer.validated_data['quantity']

                if existing_item:
                    # Nếu đã có, cộng thêm số lượng mới
                    new_quantity += existing_item.quantity

                # Kiểm tra stock với tổng số lượng
                if book['stock'] < new_quantity:
                    return Response(
                        {'error': f'Not enough stock. Available: {book["stock"]}'},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                price = Decimal(str(book['price']))

                if existing_item:
                    # Cập nhật số lượng cho item đã tồn tại
                    existing_item.quantity = new_quantity
                    existing_item.save()
                    return Response(
                        CartItemSerializer(existing_item).data,
                        status=status.HTTP_200_OK
                    )
                else:
                    # Tạo item mới nếu chưa tồn tại
                    cart_item = CartItem.objects.create(
                        cart=cart,
                        book_id=str(book_id),
                        quantity=new_quantity,
                        price_at_time=price
                    )
                    return Response(
                        CartItemSerializer(cart_item).data,
                        status=status.HTTP_201_CREATED
                    )

            except Exception as e:
                print(f"Error: {str(e)}")
                return Response(
                    {'error': f'Error adding item to cart: {str(e)}'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get_queryset(self):
        try:
            customer = Customer.objects.using('mysql').get(user_id=self.request.user.id)
            return Cart.objects.filter(customer_id=customer.id)
        except Customer.DoesNotExist:
            return Cart.objects.none()

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