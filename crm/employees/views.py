from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import (
    Employee, EmployeePerformance, EmployeeActivity, EmployeeGoal,
    EmployeeTraining, EmployeeSchedule, EmployeeMetrics
)
from .serializers import (
    EmployeeSerializer, EmployeePerformanceSerializer, EmployeeActivitySerializer,
    EmployeeGoalSerializer, EmployeeTrainingSerializer, EmployeeScheduleSerializer,
    EmployeeMetricsSerializer
)
from django.db.models import Avg


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['role', 'department', 'status', 'company', 'manager']
    search_fields = ['user__first_name', 'user__last_name', 'employee_id']
    ordering_fields = ['hire_date', 'created_at', 'user__last_name']
    ordering = ['user__last_name', 'user__first_name']

    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        employee = self.get_object()
        employee.status = 'active'
        employee.save()
        return Response({'status': 'Employee activated'})

    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        employee = self.get_object()
        employee.status = 'inactive'
        employee.save()
        return Response({'status': 'Employee deactivated'})


class EmployeePerformanceViewSet(viewsets.ModelViewSet):
    queryset = EmployeePerformance.objects.all()
    serializer_class = EmployeePerformanceSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['employee', 'period_start', 'period_end', 'reviewed_by']
    search_fields = ['employee__user__first_name', 'employee__user__last_name']
    ordering_fields = ['period_end', 'overall_rating', 'created_at']
    ordering = ['-period_end']


class EmployeeActivityViewSet(viewsets.ModelViewSet):
    queryset = EmployeeActivity.objects.all()
    serializer_class = EmployeeActivitySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['employee', 'activity_type', 'related_customer', 'related_company']
    search_fields = ['description', 'employee__user__first_name']
    ordering_fields = ['timestamp', 'created_at']
    ordering = ['-timestamp']


class EmployeeGoalViewSet(viewsets.ModelViewSet):
    queryset = EmployeeGoal.objects.all()
    serializer_class = EmployeeGoalSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['employee', 'goal_type', 'status', 'target_date']
    search_fields = ['title', 'description']
    ordering_fields = ['target_date', 'progress_percentage', 'created_at']
    ordering = ['target_date']

    @action(detail=True, methods=['post'])
    def update_progress(self, request, pk=None):
        goal = self.get_object()
        progress = request.data.get('progress')
        if progress is not None:
            goal.progress_percentage = progress
            if progress >= 100:
                goal.status = 'completed'
            elif progress > 0:
                goal.status = 'in_progress'
            goal.save()
            return Response({'status': 'Progress updated'})
        return Response({'error': 'Progress value required'}, status=status.HTTP_400_BAD_REQUEST)


class EmployeeTrainingViewSet(viewsets.ModelViewSet):
    queryset = EmployeeTraining.objects.all()
    serializer_class = EmployeeTrainingSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['employee', 'training_type', 'status', 'provider']
    search_fields = ['title', 'description']
    ordering_fields = ['start_date', 'end_date', 'score', 'created_at']
    ordering = ['-start_date']

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        training = self.get_object()
        score = request.data.get('score')
        training.status = 'completed'
        if score is not None:
            training.score = score
        training.save()
        return Response({'status': 'Training completed'})


class EmployeeScheduleViewSet(viewsets.ModelViewSet):
    queryset = EmployeeSchedule.objects.all()
    serializer_class = EmployeeScheduleSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['employee', 'date', 'is_working_day']
    search_fields = ['employee__user__first_name', 'employee__user__last_name']
    ordering_fields = ['date', 'start_time', 'end_time']
    ordering = ['date', 'start_time']


class EmployeeMetricsViewSet(viewsets.ModelViewSet):
    queryset = EmployeeMetrics.objects.all()
    serializer_class = EmployeeMetricsSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['employee', 'date']
    search_fields = ['employee__user__first_name', 'employee__user__last_name']
    ordering_fields = ['date', 'efficiency_score', 'quality_score']
    ordering = ['-date']

    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Get employee metrics summary"""
        total_employees = self.get_queryset().values('employee').distinct().count()
        avg_efficiency = self.get_queryset().aggregate(
            avg_efficiency=Avg('efficiency_score')
        )['avg_efficiency'] or 0
        avg_quality = self.get_queryset().aggregate(
            avg_quality=Avg('quality_score')
        )['avg_quality'] or 0
        
        return Response({
            'total_employees': total_employees,
            'average_efficiency': avg_efficiency,
            'average_quality': avg_quality
        })
