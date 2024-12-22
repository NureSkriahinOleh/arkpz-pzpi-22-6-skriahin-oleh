from rest_framework import serializers
from .models import IncidentReport

class IncidentReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = IncidentReport
        fields = '__all__'
        read_only_fields = ['created_at']