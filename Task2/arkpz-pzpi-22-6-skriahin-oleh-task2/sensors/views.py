from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Sensor, SensorLog
from .serializers import SensorSerializer, SensorLogSerializer


# Ця в'юшка дозволяє отримувати список сенсорів або створювати новий сенсор.
class SensorListView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]  # Дозвіл доступу для всіх користувачів
    queryset = Sensor.objects.all()  # Всі сенсори з бази даних
    serializer_class = SensorSerializer

    @swagger_auto_schema(
        responses={200: SensorSerializer(many=True)},  # Відповідь із списком сенсорів
        operation_description="Отримати список усіх сенсорів."
    )
    def get(self, request):
        """
        Отримати список усіх сенсорів.
        """
        sensors = self.get_queryset()
        serializer = self.get_serializer(sensors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=SensorSerializer,  # Тіло запиту для створення сенсора
        responses={201: SensorSerializer, 400: "Validation error"},  # Можливі відповіді
        operation_description="Створити новий сенсор."
    )
    def post(self, request):
        """
        Створити новий сенсор.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Дозволяє отримати, оновити або видалити конкретний сенсор за його ID.
class SensorDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]  # Доступ тільки для авторизованих користувачів
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer

    @swagger_auto_schema(
        responses={200: SensorSerializer, 404: "Sensor not found"},
        operation_description="Отримати детальну інформацію про сенсор за його ID."
    )
    def get(self, request, pk):
        """
        Отримати деталі сенсора за ID.
        """
        return super().get(request, pk)

    @swagger_auto_schema(
        request_body=SensorSerializer,  # Тіло запиту для оновлення
        responses={200: SensorSerializer, 400: "Validation error", 404: "Sensor not found"},
        operation_description="Оновити дані сенсора."
    )
    def put(self, request, pk):
        """
        Оновити дані сенсора за ID.
        """
        return super().put(request, pk)

    @swagger_auto_schema(
        responses={204: "Sensor successfully deleted", 404: "Sensor not found"},
        operation_description="Видалити сенсор за його ID."
    )
    def delete(self, request, pk):
        """
        Видалити сенсор за ID.
        """
        return super().delete(request, pk)


# Дозволяє отримати список логів конкретного сенсора або додати новий лог.
class SensorLogListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]  # Доступ лише для авторизованих користувачів
    serializer_class = SensorLogSerializer

    @swagger_auto_schema(
        responses={200: SensorLogSerializer(many=True)},  # Список логів
        operation_description="Отримати список логів для конкретного сенсора."
    )
    def get(self, request, sensor_id):
        """
        Отримати список логів для сенсора за його ID.
        """
        logs = SensorLog.objects.filter(sensor_id=sensor_id)  # Фільтруємо логи по сенсору
        serializer = self.get_serializer(logs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=SensorLogSerializer,  # Тіло запиту для створення лога
        responses={201: SensorLogSerializer, 400: "Validation error", 404: "Sensor not found"},
        operation_description="Додати новий лог для сенсора."
    )
    def post(self, request, sensor_id):
        """
        Додати новий лог для сенсора.
        """
        try:
            sensor = Sensor.objects.get(pk=sensor_id)  # Знаходимо сенсор за ID
        except Sensor.DoesNotExist:
            return Response({"error": "Sensor not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(sensor=sensor)  # Задаємо поле sensor
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Дозволяє отримати, оновити або видалити конкретний лог сенсора.
class SensorLogDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]  # Доступ лише для авторизованих користувачів
    queryset = SensorLog.objects.all()
    serializer_class = SensorLogSerializer

    @swagger_auto_schema(
        responses={200: SensorLogSerializer, 404: "Log not found"},
        operation_description="Отримати деталі конкретного лога сенсора."
    )
    def get(self, request, pk):
        """
        Отримати деталі лога сенсора за ID.
        """
        return super().get(request, pk)

    @swagger_auto_schema(
        request_body=SensorLogSerializer,  # Тіло запиту для оновлення лога
        responses={200: SensorLogSerializer, 400: "Validation error", 404: "Log not found"},
        operation_description="Оновити дані лога сенсора."
    )
    def put(self, request, pk):
        """
        Оновити дані лога сенсора за ID.
        """
        return super().put(request, pk)

    @swagger_auto_schema(
        responses={204: "Log successfully deleted", 404: "Log not found"},
        operation_description="Видалити лог сенсора за його ID."
    )
    def delete(self, request, pk):
        """
        Видалити лог сенсора за ID.
        """
        return super().delete(request, pk)
