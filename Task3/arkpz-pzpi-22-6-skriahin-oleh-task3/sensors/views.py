from drf_yasg.utils import swagger_auto_schema
from django.http import JsonResponse
from django.views import View
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.core.mail import send_mail
from drf_yasg import openapi
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
import json
from .models import *
from .serializers import *
from users.models import *

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
        Отримати список усіх сенсорів.python manage.py inspectdb > models_dump.py
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



class CreateSensorLogAPIView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Создать новый лог для сенсора",
        request_body=CreateSensorLogSerializer,
        responses={
            201: openapi.Response(description="Успішно створено лог"),
            400: openapi.Response(description="Некоректні дані"),
            404: openapi.Response(description="Сенсор не знайдено"),
        }
    )
    def post(self, request, *args, **kwargs):
        sensor_id = request.data.get('sensor_id')
        value = request.data.get('value')

        if not sensor_id or value is None:
            return Response({"error": "sensor_id and value are required"}, status=status.HTTP_400_BAD_REQUEST)

        # Get the sensor instance
        sensor = get_object_or_404(Sensor, id=sensor_id)

        # Create a new log for the sensor
        log = SensorLog.objects.create(sensor=sensor, value=value)
        log.check_threshold()

        # Get other sensors in the same location
        location_sensors = Sensor.objects.filter(location=sensor.location)

        # Fetch relevant sensor logs (humidity, temperature, gas)
        temperature_log = location_sensors.filter(type='temperature').first()
        humidity_log = location_sensors.filter(type='humidity').first()
        gas_log = location_sensors.filter(type='gas').first()

        # Retrieve the latest logs for each type
        latest_temperature_value = SensorLog.objects.filter(sensor=temperature_log).order_by('-timestamp').first().value if temperature_log else None
        latest_humidity_value = SensorLog.objects.filter(sensor=humidity_log).order_by('-timestamp').first().value if humidity_log else None
        latest_gas_value = SensorLog.objects.filter(sensor=gas_log).order_by('-timestamp').first().value if gas_log else None

        if latest_temperature_value is not None and latest_humidity_value is not None and latest_gas_value is not None:
            # Calculate Fire Danger Index (FDI)
            try:
                fdi = (latest_temperature_value * latest_gas_value) / (latest_humidity_value + 1)
                log.fdi = fdi
                log.save()

                FDI_THRESHOLD = 50
                if fdi > FDI_THRESHOLD:
                    admins = User.objects.filter(role='admin')  # Get all admin users
                    admin_emails = admins.values_list('email', flat=True)

                    # Send email notification
                    if admin_emails:
                        send_mail(
                            subject="Fire Danger Alert",
                            message=f"""
                                Fire danger detected in location: {sensor.location}.
                                Details:
                                - Temperature: {latest_temperature_value}
                                - Humidity: {latest_humidity_value}
                                - Gas Concentration: {latest_gas_value}
                                - Fire Danger Index (FDI): {fdi}
                            """,
                            from_email="smartshield1@zohomail.eu",
                            recipient_list=admin_emails,
                        )
                        
                return Response({
                    "message": "Sensor log created successfully",
                    "log": {
                        "id": log.id,
                        "sensor": sensor.id,
                        "value": log.value,
                        "exceeded_threshold": log.exceeded_threshold,
                        "fdi": fdi,
                        "temperature": latest_temperature_value,
                        "gas": latest_gas_value,
                        "humidity": latest_humidity_value,
                    }
                }, status=status.HTTP_201_CREATED)

            except Exception as e:
                return Response({"error": f"An error occurred while calculating FDI: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"message": "Log created successfully but FDI could not be calculated due to missing data"}, status=status.HTTP_201_CREATED)
