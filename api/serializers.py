from rest_framework import serializers
from rest_framework.authtoken.views import Token
from django.contrib.auth.models import User
from .models import FlightInformation, Timeslot, UserProfile, Driver


class FlightInformationSerializer(serializers.ModelSerializer):
        class Meta:
             model = Timeslot
             fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    google_id = serializers.CharField(source='userprofile.google_id', read_only=True)
    phone_number = serializers.CharField(source='userprofile.phone_number')
    profile_picture_url = serializers.URLField(source='userprofile.profile_picture_url', read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'google_id', 'phone_number', 'profile_picture_url']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email']
        )
        google_id = self.initial_data.get('google_id')
        UserProfile.objects.create(user=user, google_id=google_id)
        Token.objects.create(user=user)
        return user

        
class TimeSlotSerializer(serializers.ModelSerializer):
        class Meta:
             model = Timeslot
             fields = '__all__'

class DriverSerializer(serializers.ModelSerializer):
        user = serializers.HiddenField(default=serializers.CurrentUserDefault())

        class Meta:
             model = Driver
             fields = '__all__'
     