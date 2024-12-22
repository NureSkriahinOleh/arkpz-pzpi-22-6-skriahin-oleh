from django.db import models

class Sensor(models.Model):
    SENSOR_TYPE_CHOICES = [
        ('motion', 'Motion'),
        ('smoke', 'Smoke'),
        ('temperature', 'Temperature'),
    ]
    type = models.CharField(max_length=20, choices=SENSOR_TYPE_CHOICES)
    location = models.CharField(max_length=255)
    status = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.type} sensor at {self.location}"

class SensorLog(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, related_name='logs')
    value = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    exceeded_threshold = models.BooleanField(default=False)

    def __str__(self):
        return f"Log for {self.sensor} at {self.timestamp}"
