from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from .models import IncidentReport
from .serializers import IncidentReportSerializer

# Отримання списку інцидентів або створення нового інциденту.
class IncidentReportListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = IncidentReportSerializer

    def get_queryset(self):
        # Повертає інциденти. Можлива фільтрація за параметрами.
        queryset = IncidentReport.objects.all()
        incident_type = self.request.query_params.get('type')
        if incident_type:
            queryset = queryset.filter(type=incident_type)
        return queryset.order_by('-created_at')

    @swagger_auto_schema(
        responses={200: IncidentReportSerializer(many=True)},
        operation_description="Retrieve a list of incident reports with optional filtering by type."
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=IncidentReportSerializer,
        responses={201: IncidentReportSerializer, 400: "Validation error"},
        operation_description="Create a new incident report."
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

# Отримання, оновлення або видалення конкретного інциденту.
class IncidentReportDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = IncidentReportSerializer

    def get_queryset(self):
        # Повертає інцидент для користувача
        return IncidentReport.objects.all()

    @swagger_auto_schema(
        responses={200: IncidentReportSerializer, 404: "Incident not found"},
        operation_description="Retrieve details of a specific incident report."
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=IncidentReportSerializer,
        responses={200: IncidentReportSerializer, 400: "Validation error", 404: "Incident not found"},
        operation_description="Update details of a specific incident report."
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        responses={204: "Incident successfully deleted", 404: "Incident not found"},
        operation_description="Delete a specific incident report."
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
