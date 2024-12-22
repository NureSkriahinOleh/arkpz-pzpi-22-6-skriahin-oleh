from django.db import models
from sensors.models import Sensor
from cameras.models import Camera

class IncidentReport(models.Model):
    INCIDENT_TYPE_CHOICES = [
        ('fire', 'Fire'),
        ('gas_leak', 'Gas Leak'),
        ('intrusion', 'Intrusion'),
    ]
    type = models.CharField(max_length=20, choices=INCIDENT_TYPE_CHOICES)
    details = models.TextField()
    sensor = models.ForeignKey(Sensor, on_delete=models.SET_NULL, null=True, blank=True, related_name='incidents')
    camera = models.ForeignKey(Camera, on_delete=models.SET_NULL, null=True, blank=True, related_name='incidents')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Incident: {self.type} at {self.created_at}"
