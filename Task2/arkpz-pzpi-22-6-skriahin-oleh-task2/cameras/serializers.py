from rest_framework import serializers
from .models import Camera, CameraLog

class CameraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Camera
        fields = ['id', 'location', 'status']

class CameraLogSerializer(serializers.ModelSerializer):
    camera = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = CameraLog
        fields = ['id', 'camera', 'file_path', 'recorded_at']
