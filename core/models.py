from django.db import models
from django.utils.timezone import now

class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.name


class Appointment(models.Model):
    SERVICE_CHOICES = [
        ('Quick Consultation', 'Quick Consultation'),
        ('Full Consultation', 'Full Consultation'),
    ]
    
    name = models.CharField(max_length=100)
    email = models.EmailField()
    service = models.CharField(max_length=50, choices=SERVICE_CHOICES)
    date = models.DateField(default=now)
    time = models.TimeField(default=now)
    status = models.CharField(max_length=20, default="Pending", choices=[("Pending", "Pending"), ("Confirmed", "Confirmed")])

    def __str__(self):
        return f"{self.name} - {self.service} on {self.date} at {self.time}"

