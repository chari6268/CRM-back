from rest_framework import serializers
from .models import (
    Employee, EmployeePerformance, EmployeeActivity, EmployeeGoal,
    EmployeeTraining, EmployeeSchedule, EmployeeMetrics
)
from crm.core.serializers import UserSerializer, CompanySerializer, CustomerSerializer


class EmployeeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    company = CompanySerializer(read_only=True)
    manager = 'self'  # Self-referencing relationship
    
    class Meta:
        model = Employee
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class EmployeePerformanceSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer(read_only=True)
    reviewed_by = EmployeeSerializer(read_only=True)
    
    class Meta:
        model = EmployeePerformance
        fields = '__all__'
        read_only_fields = ['id', 'created_at']


class EmployeeActivitySerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer(read_only=True)
    related_customer = CustomerSerializer(read_only=True)
    related_company = CompanySerializer(read_only=True)
    
    class Meta:
        model = EmployeeActivity
        fields = '__all__'
        read_only_fields = ['id', 'timestamp', 'created_at']


class EmployeeGoalSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer(read_only=True)
    
    class Meta:
        model = EmployeeGoal
        fields = '__all__'
        read_only_fields = ['id', 'start_date', 'created_at']


class EmployeeTrainingSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer(read_only=True)
    
    class Meta:
        model = EmployeeTraining
        fields = '__all__'
        read_only_fields = ['id', 'start_date', 'created_at']


class EmployeeScheduleSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer(read_only=True)
    
    class Meta:
        model = EmployeeSchedule
        fields = '__all__'
        read_only_fields = ['id', 'created_at']


class EmployeeMetricsSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer(read_only=True)
    
    class Meta:
        model = EmployeeMetrics
        fields = '__all__'
        read_only_fields = ['id', 'date', 'created_at']
