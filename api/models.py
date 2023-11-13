from django.contrib.auth.models import User
from django.conf import settings
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    google_id = models.CharField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=10, default=0)
    profile_picture_url = models.URLField(max_length=255, null=True, blank=True)

class FlightInformation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    ride_type = models.CharField(max_length=10)
    flight_time = models.TimeField()
    flight_date = models.DateField()
    dropoff_point = models.CharField(max_length=20)
    airline = models.CharField(max_length=30)

    def __str__(self):
        return self.ride_type

class Timeslot(models.Model):
    date = models.DateField()
    time = models.TimeField()
    space_available = models.IntegerField()
    user = models.CharField(max_length=100)

class Driver(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None)
    carModel = models.CharField(max_length = 50)
    carColor = models.CharField(max_length = 50)
    licensePlate = models.CharField(max_length = 50)