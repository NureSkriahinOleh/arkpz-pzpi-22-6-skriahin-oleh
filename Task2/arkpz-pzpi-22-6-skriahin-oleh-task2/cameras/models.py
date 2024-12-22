from django.db import models

class Camera(models.Model):
    location = models.CharField(max_length=255)
    status = models.BooleanField(default=True)

    def __str__(self):
        return f"Camera at {self.location}"

class CameraLog(models.Model):
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE, related_name='logs')
    file_path = models.CharField(max_length=255)
    recorded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Video log for {self.camera} at {self.recorded_at}"