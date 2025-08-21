from rest_framework import serializers
from .models import (
    Contact, CustomerSegment, CustomerTag, CustomerActivity,
    CustomerPreference, CustomerDocument
)
from crm.core.serializers import CustomerSerializer, CompanySerializer


class ContactSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    
    class Meta:
        model = Contact
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class CustomerSegmentSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)
    customers = CustomerSerializer(many=True, read_only=True)
    
    class Meta:
        model = CustomerSegment
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class CustomerTagSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)
    
    class Meta:
        model = CustomerTag
        fields = '__all__'
        read_only_fields = ['id', 'created_at']


class CustomerActivitySerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    company = CompanySerializer(read_only=True)
    
    class Meta:
        model = CustomerActivity
        fields = '__all__'
        read_only_fields = ['id', 'timestamp', 'created_at']


class CustomerPreferenceSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    company = CompanySerializer(read_only=True)
    
    class Meta:
        model = CustomerPreference
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class CustomerDocumentSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    company = CompanySerializer(read_only=True)
    
    class Meta:
        model = CustomerDocument
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']
