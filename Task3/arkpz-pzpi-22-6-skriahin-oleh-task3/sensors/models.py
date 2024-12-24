from django.db import models

SENSOR_TYPE_CHOICES = [
    ('motion', 'Motion'),
    ('smoke', 'Smoke'),
    ('temperature', 'Temperature'),
    ('humidity', 'Humidity'),
    ('gas', 'Gas'),
]

class Sensor(models.Model):
    type = models.CharField(max_length=20, choices=SENSOR_TYPE_CHOICES)
    location = models.CharField(max_length=255)
    status = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.type} sensor at {self.location}"

class SensorLog(models.Model):
    id = models.BigAutoField(primary_key=True)
    value = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    exceeded_threshold = models.BooleanField(default=False)
    sensor = models.ForeignKey('Sensor', on_delete=models.CASCADE)

    class Meta:
        db_table = 'sensors_sensorlog'

    def check_threshold(self):
        try:
            threshold = Threshold.objects.get(type=self.sensor.type)
            if self.sensor.type == 'humidity':
                self.exceeded_threshold = self.value < threshold.threshold_value
            else:
                self.exceeded_threshold = self.value > threshold.threshold_value
        except Threshold.DoesNotExist:
            self.exceeded_threshold = False
        self.save()


class Threshold(models.Model):
    type = models.CharField(max_length=20, choices=SENSOR_TYPE_CHOICES)
    threshold_value = models.FloatField()

    class Meta:
        db_table = 'thresholds'
