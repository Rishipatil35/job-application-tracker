from django.db.models import Q
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import JobApplication
from .serializers import JobApplicationSerializer


class ApplicationViewSet(viewsets.ModelViewSet):
    """CRUD API. Every query is limited to the logged-in user's records."""
    serializer_class = JobApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = JobApplication.objects.filter(user=self.request.user)
        q = self.request.query_params.get('q', '').strip()
        status = self.request.query_params.get('status', '').strip()
        if q:
            queryset = queryset.filter(Q(company__icontains=q) | Q(role__icontains=q))
        if status in JobApplication.Status.values:
            queryset = queryset.filter(status=status)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def stats(self, request):
        queryset = JobApplication.objects.filter(user=request.user)
        return Response({
            'total': queryset.count(),
            'applied': queryset.filter(status='applied').count(),
            'interviews': queryset.filter(status='interview').count(),
            'offers': queryset.filter(status='offer').count(),
            'rejected': queryset.filter(status='rejected').count(),
        })
