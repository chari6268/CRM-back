from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Avg, Count, Sum
from .models import (
    Contact, CustomerSegment, CustomerTag, CustomerActivity,
    CustomerPreference, CustomerDocument
)
from .serializers import (
    ContactSerializer, CustomerSegmentSerializer, CustomerTagSerializer,
    CustomerActivitySerializer, CustomerPreferenceSerializer, CustomerDocumentSerializer
)


class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = []  # Temporarily allow all access for development
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['customer', 'contact_type', 'is_primary']
    search_fields = ['first_name', 'last_name', 'email', 'phone']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']


class CustomerSegmentViewSet(viewsets.ModelViewSet):
    queryset = CustomerSegment.objects.all()
    serializer_class = CustomerSegmentSerializer
    permission_classes = []  # Temporarily allow all access for development
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['company', 'is_active']
    search_fields = ['name', 'description']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

    @action(detail=True, methods=['get'])
    def customers(self, request, pk=None):
        """Get customers in this segment"""
        segment = self.get_object()
        customers = segment.customers.all()
        from crm.core.serializers import CustomerSerializer
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)


class CustomerTagViewSet(viewsets.ModelViewSet):
    queryset = CustomerTag.objects.all()
    serializer_class = CustomerTagSerializer
    permission_classes = []  # Temporarily allow all access for development
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['company', 'color']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']


class CustomerActivityViewSet(viewsets.ModelViewSet):
    queryset = CustomerActivity.objects.all()
    serializer_class = CustomerActivitySerializer
    permission_classes = []  # Temporarily allow all access for development
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['customer', 'activity_type', 'company']
    search_fields = ['description', 'customer__name']
    ordering_fields = ['timestamp', 'created_at']
    ordering = ['-timestamp']


class CustomerPreferenceViewSet(viewsets.ModelViewSet):
    queryset = CustomerPreference.objects.all()
    serializer_class = CustomerPreferenceSerializer
    permission_classes = []  # Temporarily allow all access for development
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['customer', 'preference_type', 'company']
    search_fields = ['customer__name', 'value']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']


class CustomerDocumentViewSet(viewsets.ModelViewSet):
    queryset = CustomerDocument.objects.all()
    serializer_class = CustomerDocumentSerializer
    permission_classes = []  # Temporarily allow all access for development
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['customer', 'document_type', 'company']
    search_fields = ['title', 'description', 'customer__name']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

    @action(detail=True, methods=['post'])
    def download(self, request, pk=None):
        """Simulate document download"""
        document = self.get_object()
        # Here you would implement actual file download logic
        return Response({'status': f'Downloading {document.title}'})
