from django.contrib.auth.models import User
from django.conf import settings
from django.db import models


class UserProfile(models.Model):
    user = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=10, default=0)
    profile_picture_url = models.URLField(max_length=255, null=True, blank=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)

class FlightInformation(models.Model):
    user = models.CharField(max_length=100)    
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
    user = models.CharField(max_length=100)
    carModel = models.CharField(max_length = 50)
    carColor = models.CharField(max_length = 50)
    licensePlate = models.CharField(max_length = 50)