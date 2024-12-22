from rest_framework import serializers
from .models import Sensor, SensorLog

class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = ['id', 'type', 'location', 'status']

class SensorLogSerializer(serializers.ModelSerializer):
    sensor = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = SensorLog
        fields = ['id', 'sensor', 'value', 'timestamp', 'exceeded_threshold']