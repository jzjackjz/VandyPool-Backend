from rest_framework import serializers
from rest_framework.authtoken.views import Token
from django.contrib.auth.models import User
from .models import FlightInformation, Timeslot, UserProfile, Driver


class FlightInformationSerializer(serializers.ModelSerializer):
        class Meta:
             model = FlightInformation
             fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
        class Meta:
             model = UserProfile
             fields = '__all__'

        
class TimeSlotSerializer(serializers.ModelSerializer):
        class Meta:
             model = Timeslot
             fields = '__all__'

class DriverSerializer(serializers.ModelSerializer):
        class Meta:
             model = Driver
             fields = '__all__'
     
