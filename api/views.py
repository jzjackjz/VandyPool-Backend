from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout
from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, action, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter
from .models import FlightInformation, Timeslot, UserProfile, Driver
from .serializers import FlightInformationSerializer, UserSerializer, TimeSlotSerializer, DriverSerializer
from google.oauth2 import id_token
from google.auth.transport import requests
from decouple import config


@api_view(['POST'])
def google_register(request):
    try:
        idinfo = id_token.verify_oauth2_token(request.data['token'], requests.Request(), config('GOOGLE_CLIENT_ID'))

        userid = idinfo['sub']
        email = idinfo.get('email')
        first_name = idinfo.get('given_name', '')
        last_name = idinfo.get('family_name', '')
        profile_picture_url = idinfo.get('picture', '')

        if not User.objects.filter(email=email).exists():
            user = User.objects.create_user(username=email, email=email, first_name=first_name, last_name=last_name)
            token, created = Token.objects.get_or_create(user=user)

            return Response({'status': 'success', 'user_id': user.id, 'sessionToken': token.key}, status=status.HTTP_201_CREATED)
        else:
            return Response({'status': 'error', 'message': 'User already exists'}, status=status.HTTP_409_CONFLICT)

    except ValueError:
        return Response({'status': 'error', 'message': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def google_login(request):
    try:
        idinfo = id_token.verify_oauth2_token(request.data['token'], requests.Request(), config('GOOGLE_CLIENT_ID'))
        userid = idinfo['sub']
        email = idinfo.get('email')

        try:
            user = User.objects.get(email=email)
            token, created = Token.objects.get_or_create(user=user)
            return Response({'status': 'success', 'user_id': user.id, 'sessionToken': token.key}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'status': 'error', 'message': 'User does not exist. Please sign up.'}, status=status.HTTP_404_NOT_FOUND)

    except ValueError:
        return Response({'status': 'error', 'message': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def logout_view(request):
    request.user.auth_token.delete()
    
    return Response({"status": "success", "message": "Logged out successfully"})





class FlightInformationViewSet(viewsets.ModelViewSet):
    queryset = FlightInformation.objects.all()
    serializer_class = FlightInformationSerializer

    def get_queryset(self):
        username = self.request.query_params.get('username', None)
        if username:
            return FlightInformation.objects.filter(user=username)
        return FlightInformation.objects.all()

class UserViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer
    
    def get_queryset(self):
        username = self.request.query_params.get('username', None)
        if username:
            return UserProfile.objects.filter(user=username)
        return UserProfile.objects.all()

class TimeslotViewSet(viewsets.ModelViewSet):
    queryset = Timeslot.objects.all()
    serializer_class = TimeSlotSerializer

    def get_queryset(self):
        username = self.request.query_params.get('username', None)
        if username:
            return Timeslot.objects.filter(user=username)
        return Timeslot.objects.all()
    
class DriverViewSet(viewsets.ModelViewSet):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer

    def get_queryset(self):
        username = self.request.query_params.get('username', None)
        if username:
            return Driver.objects.filter(user=username)
        return Driver.objects.all()
