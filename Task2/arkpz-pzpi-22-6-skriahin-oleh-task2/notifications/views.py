from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from .models import Notification
from .serializers import NotificationSerializer

# Отримання списку сповіщень або створення нового сповіщення.
class NotificationListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationSerializer

    def get_queryset(self):
        # Повернення списку сповіщень для конкретного користувача
        return Notification.objects.filter(user=self.request.user)

    @swagger_auto_schema(
        responses={200: NotificationSerializer(many=True)},
        operation_description="Retrieve a list of notifications for the authenticated user."
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=NotificationSerializer,
        responses={201: NotificationSerializer, 400: "Validation error"},
        operation_description="Create a new notification for the authenticated user."
    )
    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        data['user'] = request.user.id
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Отримання, оновлення або видалення сповіщення.
class NotificationDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationSerializer

    def get_queryset(self):
        # Виборка сповіщень користувача
        return Notification.objects.filter(user=self.request.user)

    @swagger_auto_schema(
        responses={200: NotificationSerializer, 404: "Notification not found"},
        operation_description="Retrieve details of a specific notification."
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=NotificationSerializer,
        responses={200: NotificationSerializer, 400: "Validation error", 404: "Notification not found"},
        operation_description="Update details of a specific notification."
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        responses={204: "Notification successfully deleted", 404: "Notification not found"},
        operation_description="Delete a specific notification."
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
