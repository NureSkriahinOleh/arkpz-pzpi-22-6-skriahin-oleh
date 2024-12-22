from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('guard', 'Guard'),
        ('visitor', 'Visitor'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='visitor')
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.username