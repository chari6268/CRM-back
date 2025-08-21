from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta
from .models import User, Company, Customer, Interaction, Task, Notification
from .serializers import (
    UserSerializer, CompanySerializer, CustomerSerializer,
    InteractionSerializer, TaskSerializer, NotificationSerializer,
    DashboardStatsSerializer
)


def root_view(request):
    """Serve the React frontend at the root URL"""
    return render(request, 'index.html')


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet for User model."""
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    permission_classes = []  # Temporarily allow all access for development
    filterset_fields = ['department', 'position']
    search_fields = ['username', 'first_name', 'last_name', 'email']
    ordering_fields = ['username', 'first_name', 'last_name', 'created_at']

    @action(detail=False, methods=['get'])
    def me(self, request):
        """Get current user information."""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def departments(self, request):
        """Get list of departments."""
        departments = User.objects.filter(
            is_active=True
        ).values_list('department', flat=True).distinct().exclude(department='')
        return Response(list(departments))


class CompanyViewSet(viewsets.ModelViewSet):
    """ViewSet for Company model."""
    queryset = Company.objects.filter(is_active=True)
    serializer_class = CompanySerializer
    permission_classes = []  # Temporarily allow all access for development
    filterset_fields = ['industry', 'size']
    search_fields = ['name', 'industry', 'website']
    ordering_fields = ['name', 'created_at']

    @action(detail=True, methods=['get'])
    def customers(self, request, pk=None):
        """Get customers for a specific company."""
        company = self.get_object()
        customers = company.customers.filter(is_active=True)
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def industries(self, request):
        """Get list of industries."""
        industries = Company.objects.filter(
            is_active=True
        ).values_list('industry', flat=True).distinct().exclude(industry='')
        return Response(list(industries))


class CustomerViewSet(viewsets.ModelViewSet):
    """ViewSet for Customer model."""
    queryset = Customer.objects.filter(is_active=True)
    serializer_class = CustomerSerializer
    permission_classes = []  # Temporarily allow all access for development
    filterset_fields = ['status', 'source', 'assigned_to', 'company']
    search_fields = ['first_name', 'last_name', 'email', 'company__name']
    ordering_fields = ['first_name', 'last_name', 'created_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        # Filter by assigned user if specified
        assigned_to = self.request.query_params.get('assigned_to', None)
        if assigned_to:
            queryset = queryset.filter(assigned_to=assigned_to)
        return queryset

    @action(detail=True, methods=['get'])
    def interactions(self, request, pk=None):
        """Get interactions for a specific customer."""
        customer = self.get_object()
        interactions = customer.interactions.all()
        serializer = InteractionSerializer(interactions, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def timeline(self, request, pk=None):
        """Get customer timeline with interactions and tasks."""
        customer = self.get_object()
        
        # Get interactions
        interactions = customer.interactions.all().order_by('-date')
        # Get tasks
        tasks = customer.tasks.all().order_by('-created_at')
        
        timeline = []
        
        for interaction in interactions:
            timeline.append({
                'type': 'interaction',
                'id': interaction.id,
                'title': interaction.subject,
                'description': interaction.description,
                'date': interaction.date,
                'user': interaction.user.get_full_name(),
                'interaction_type': interaction.type
            })
        
        for task in tasks:
            timeline.append({
                'type': 'task',
                'id': task.id,
                'title': task.title,
                'description': task.description,
                'date': task.created_at,
                'user': task.assigned_to.get_full_name(),
                'status': task.status,
                'priority': task.priority
            })
        
        # Sort by date
        timeline.sort(key=lambda x: x['date'], reverse=True)
        
        return Response(timeline)

    @action(detail=False, methods=['get'])
    def status_counts(self, request):
        """Get customer counts by status."""
        status_counts = Customer.objects.filter(
            is_active=True
        ).values('status').annotate(count=Count('id'))
        return Response(status_counts)


class InteractionViewSet(viewsets.ModelViewSet):
    """ViewSet for Interaction model."""
    queryset = Interaction.objects.all()
    serializer_class = InteractionSerializer
    permission_classes = []  # Temporarily allow all access for development
    filterset_fields = ['type', 'customer', 'user']
    search_fields = ['subject', 'description', 'customer__first_name', 'customer__last_name']
    ordering_fields = ['date', 'created_at']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TaskViewSet(viewsets.ModelViewSet):
    """ViewSet for Task model."""
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = []  # Temporarily allow all access for development
    filterset_fields = ['status', 'priority', 'assigned_to', 'customer']
    search_fields = ['title', 'description']
    ordering_fields = ['due_date', 'created_at', 'priority']

    def get_queryset(self):
        queryset = super().get_queryset()
        # Filter by assigned user if specified
        assigned_to = self.request.query_params.get('assigned_to', None)
        if assigned_to:
            queryset = queryset.filter(assigned_to=assigned_to)
        return queryset

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """Mark task as completed."""
        task = self.get_object()
        task.status = 'completed'
        task.completed_at = timezone.now()
        task.save()
        serializer = self.get_serializer(task)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def overdue(self, request):
        """Get overdue tasks."""
        overdue_tasks = Task.objects.filter(
            due_date__lt=timezone.now(),
            status__in=['pending', 'in_progress']
        )
        serializer = self.get_serializer(overdue_tasks, many=True)
        return Response(serializer.data)


class NotificationViewSet(viewsets.ModelViewSet):
    """ViewSet for Notification model."""
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = []  # Temporarily allow all access for development

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        """Mark notification as read."""
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        serializer = self.get_serializer(notification)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        """Mark all notifications as read."""
        self.get_queryset().update(is_read=True)
        return Response({'status': 'success'})


class DashboardViewSet(viewsets.ViewSet):
    """ViewSet for dashboard data."""
    permission_classes = []  # Temporarily allow all access for development

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get dashboard statistics."""
        # Get basic counts
        total_customers = Customer.objects.filter(is_active=True).count()
        total_companies = Company.objects.filter(is_active=True).count()
        active_tasks = Task.objects.filter(status__in=['pending', 'in_progress']).count()
        pending_interactions = Interaction.objects.filter(
            date__gte=timezone.now() - timedelta(days=7)
        ).count()

        # Get recent activities
        recent_interactions = Interaction.objects.select_related(
            'customer', 'user'
        ).order_by('-date')[:10]
        
        recent_activities = []
        for interaction in recent_interactions:
            recent_activities.append({
                'type': 'interaction',
                'id': interaction.id,
                'title': f"{interaction.type.title()} with {interaction.customer.full_name}",
                'date': interaction.date,
                'user': interaction.user.get_full_name()
            })

        # Get upcoming deadlines
        upcoming_tasks = Task.objects.filter(
            due_date__gte=timezone.now(),
            status__in=['pending', 'in_progress']
        ).order_by('due_date')[:10]
        
        upcoming_deadlines = []
        for task in upcoming_tasks:
            upcoming_deadlines.append({
                'type': 'task',
                'id': task.id,
                'title': task.title,
                'due_date': task.due_date,
                'priority': task.priority,
                'assigned_to': task.assigned_to.get_full_name()
            })

        data = {
            'total_customers': total_customers,
            'total_companies': total_companies,
            'active_tasks': active_tasks,
            'pending_interactions': pending_interactions,
            'recent_activities': recent_activities,
            'upcoming_deadlines': upcoming_deadlines
        }

        serializer = DashboardStatsSerializer(data)
        return Response(serializer.data)
