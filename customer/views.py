# book/views.py (thêm vào file hiện có)

from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from .models import Customer
from .serializers import CustomerSerializer

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    # Sửa lại filterset_fields
    filterset_fields = ['user']  # hoặc bỏ qua user__isnull và tạo custom filter
    search_fields = ['first_name', 'last_name', 'email', 'phone']
    ordering_fields = ['created_at', 'last_name', 'first_name']
    ordering = ['-created_at']

    # Thêm method để filter customers không có user
    @action(detail=False, methods=['get'])
    def unregistered(self, request):
        """Get customers without user accounts"""
        customers = Customer.objects.filter(user__isnull=True)
        page = self.paginate_queryset(customers)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(customers, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def registered(self, request):
        """Get customers with user accounts"""
        customers = Customer.objects.filter(user__isnull=False)
        page = self.paginate_queryset(customers)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(customers, many=True)
        return Response(serializer.data)
    
