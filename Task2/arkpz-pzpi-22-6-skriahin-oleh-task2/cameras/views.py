from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from drf_yasg.utils import swagger_auto_schema
from .models import Camera, CameraLog
from .serializers import CameraSerializer, CameraLogSerializer

# Список та створення камер
class CameraListView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = Camera.objects.all()
    serializer_class = CameraSerializer

    @swagger_auto_schema(
        responses={200: CameraSerializer(many=True)},
        operation_description="Get a list of all cameras."
    )
    def get(self, request):
        """
        Отримати список усіх камер.
        """
        cameras = self.get_queryset()
        serializer = self.get_serializer(cameras, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=CameraSerializer,
        responses={201: CameraSerializer, 400: "Validation error"},
        operation_description="Create a new camera."
    )
    def post(self, request):
        """
        Створити нову камеру.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Деталі, оновлення та видалення камери
class CameraDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Camera.objects.all()
    serializer_class = CameraSerializer

    @swagger_auto_schema(
        responses={200: CameraSerializer, 404: "Camera not found"},
        operation_description="Get camera details by ID."
    )
    def get(self, request, pk):
        """
        Отримати деталі камери за ID.
        """
        return super().get(request, pk)

    @swagger_auto_schema(
        request_body=CameraSerializer,
        responses={200: CameraSerializer, 400: "Validation error", 404: "Camera not found"},
        operation_description="Update camera data."
    )
    def put(self, request, pk):
        """
        Оновити дані камери.
        """
        return super().put(request, pk)

    @swagger_auto_schema(
        responses={204: "Camera successfully deleted", 404: "Camera not found"},
        operation_description="Delete camera by ID."
    )
    def delete(self, request, pk):
        """
        Видалити камеру за ID.
        """
        return super().delete(request, pk)


# Список логів камери
class CameraLogListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CameraLogSerializer

    @swagger_auto_schema(
        responses={200: CameraLogSerializer(many=True)},
        operation_description="Get a list of logs for a camera by ID."
    )
    def get(self, request, camera_id):
        """
        Отримати список логів для камери ID.
        """
        logs = CameraLog.objects.filter(camera_id=camera_id)
        serializer = self.get_serializer(logs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=CameraLogSerializer,
        responses={201: CameraLogSerializer, 400: "Validation error", 404: "Camera not found"},
        operation_description="Add a new log for the camera."
    )
    def post(self, request, camera_id):
        """
        Додати новий лог для камери.
        """
        try:
            camera = Camera.objects.get(pk=camera_id)
        except Camera.DoesNotExist:
            return Response({"error": "Camera not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(camera=camera)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Деталі, оновлення та видалення лога камери
class CameraLogDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = CameraLog.objects.all()
    serializer_class = CameraLogSerializer

    @swagger_auto_schema(
        responses={200: CameraLogSerializer, 404: "Log not found"},
        operation_description="Get camera log details by ID."
    )
    def get(self, request, pk):
        """
        Отримати деталі лога камери за ID.
        """
        return super().get(request, pk)

    @swagger_auto_schema(
        request_body=CameraLogSerializer,
        responses={200: CameraLogSerializer, 400: "Validation error", 404: "Log not found"},
        operation_description="Update camera log data."
    )
    def put(self, request, pk):
        """
        Оновити дані лога камери.
        """
        return super().put(request, pk)

    @swagger_auto_schema(
        responses={204: "Log successfully deleted", 404: "Log not found"},
        operation_description="Delete camera log by ID."
    )
    def delete(self, request, pk):
        """
        Видалити лог камери за ID.
        """
        return super().delete(request, pk)
