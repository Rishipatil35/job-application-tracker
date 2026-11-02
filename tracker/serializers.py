from rest_framework import serializers
from .models import JobApplication


class JobApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = ['id', 'company', 'role', 'status', 'applied_date', 'job_url', 'notes', 'created_at']
        read_only_fields = ['id', 'created_at']
