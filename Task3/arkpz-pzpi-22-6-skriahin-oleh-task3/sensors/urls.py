from django.urls import path
from .views import *

urlpatterns = [
    # Ендпоінти для сенсорів
    path('sensors/', SensorListView.as_view(), name='sensor-list'),
    path('sensors/<int:pk>/', SensorDetailView.as_view(), name='sensor-detail'),

    # Ендпоінти для логов сенсорів
    path('sensors/<int:sensor_id>/logs/', SensorLogListView.as_view(), name='sensor-log-list'),
    path('sensors/logs/<int:pk>/', SensorLogDetailView.as_view(), name='sensor-log-detail'),
    path('sensors/logs/create/', CreateSensorLogAPIView.as_view(), name='sensor-log-create'),
]
