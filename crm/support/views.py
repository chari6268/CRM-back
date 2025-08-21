from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.utils import timezone
from .models import (
    SupportTicket, TicketResponse, ServiceLevelAgreement, KnowledgeBase,
    CustomerFeedback, SupportTeam, SupportMetrics
)
from .serializers import (
    SupportTicketSerializer, TicketResponseSerializer, ServiceLevelAgreementSerializer,
    KnowledgeBaseSerializer, CustomerFeedbackSerializer, SupportTeamSerializer,
    SupportMetricsSerializer
)


class SupportTicketViewSet(viewsets.ModelViewSet):
    queryset = SupportTicket.objects.all()
    serializer_class = SupportTicketSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'priority', 'ticket_type', 'assigned_to', 'customer']
    search_fields = ['title', 'description', 'ticket_number']
    ordering_fields = ['priority', 'created_at', 'due_date', 'resolved_at']
    ordering = ['-priority', '-created_at']

    @action(detail=True, methods=['post'])
    def assign(self, request, pk=None):
        ticket = self.get_object()
        user_id = request.data.get('user_id')
        if user_id:
            ticket.assigned_to_id = user_id
            ticket.save()
            return Response({'status': 'Ticket assigned'})
        return Response({'error': 'User ID required'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def resolve(self, request, pk=None):
        ticket = self.get_object()
        ticket.status = 'resolved'
        ticket.resolved_at = timezone.now()
        ticket.save()
        return Response({'status': 'Ticket resolved'})

    @action(detail=True, methods=['post'])
    def close(self, request, pk=None):
        ticket = self.get_object()
        ticket.status = 'closed'
        ticket.closed_at = timezone.now()
        ticket.save()
        return Response({'status': 'Ticket closed'})


class TicketResponseViewSet(viewsets.ModelViewSet):
    queryset = TicketResponse.objects.all()
    serializer_class = TicketResponseSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['ticket', 'user', 'is_internal']
    search_fields = ['message']
    ordering_fields = ['created_at']
    ordering = ['created_at']


class ServiceLevelAgreementViewSet(viewsets.ModelViewSet):
    queryset = ServiceLevelAgreement.objects.all()
    serializer_class = ServiceLevelAgreementSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['priority', 'is_active']
    search_fields = ['name', 'description']
    ordering_fields = ['priority', 'response_time', 'resolution_time']
    ordering = ['priority', 'response_time']


class KnowledgeBaseViewSet(viewsets.ModelViewSet):
    queryset = KnowledgeBase.objects.all()
    serializer_class = KnowledgeBaseSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'is_public', 'created_by']
    search_fields = ['title', 'content', 'tags']
    ordering_fields = ['created_at', 'updated_at', 'view_count']
    ordering = ['-created_at']

    @action(detail=True, methods=['post'])
    def increment_view(self, request, pk=None):
        article = self.get_object()
        article.view_count += 1
        article.save()
        return Response({'status': 'View count incremented'})


class CustomerFeedbackViewSet(viewsets.ModelViewSet):
    queryset = CustomerFeedback.objects.all()
    serializer_class = CustomerFeedbackSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['feedback_type', 'rating', 'customer']
    search_fields = ['title', 'description']
    ordering_fields = ['rating', 'created_at']
    ordering = ['-rating', '-created_at']


class SupportTeamViewSet(viewsets.ModelViewSet):
    queryset = SupportTeam.objects.all()
    serializer_class = SupportTeamSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['is_active', 'created_by']
    search_fields = ['name', 'description']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']


class SupportMetricsViewSet(viewsets.ModelViewSet):
    queryset = SupportMetrics.objects.all()
    serializer_class = SupportMetricsSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['date', 'team', 'metric_type']
    search_fields = ['team__name']
    ordering_fields = ['date', 'created_at']
    ordering = ['-date', '-created_at']

    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Get support metrics summary"""
        total_tickets = sum(metric.total_tickets for metric in self.get_queryset())
        resolved_tickets = sum(metric.resolved_tickets for metric in self.get_queryset())
        avg_resolution_time = sum(metric.avg_resolution_time.total_seconds() for metric in self.get_queryset() if metric.avg_resolution_time) / max(len(self.get_queryset()), 1)
        
        return Response({
            'total_tickets': total_tickets,
            'resolved_tickets': resolved_tickets,
            'resolution_rate': (resolved_tickets / total_tickets * 100) if total_tickets > 0 else 0,
            'avg_resolution_time_hours': avg_resolution_time / 3600
        })
