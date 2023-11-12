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
            UserProfile.objects.create(user=user, google_id=userid, profile_picture_url=profile_picture_url)
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

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_or_edit_phone_number(request):
    user = request.user
    phone_number = request.data.get('phone_number')

    if phone_number:
        user_profile, created = UserProfile.objects.get_or_create(user=user)
        user_profile.phone_number = phone_number
        user_profile.save()

        return Response({'status': 'success', 'phone_number': phone_number})
    else:
        return Response({'status': 'error', 'message': 'No phone number provided'}, status=status.HTTP_400_BAD_REQUEST)




class FlightInformationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication,)

    queryset = FlightInformation.objects.all()
    serializer_class = FlightInformationSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        user = self.request.user
        return FlightInformation.objects.filter(user=user)

class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication,)

    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['get'])
    def current_user(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

class TimeslotViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication,)

    queryset = Timeslot.objects.all()
    serializer_class = TimeSlotSerializer
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        user = self.request.user
        return Timeslot.objects.filter(user=user)
    
class DriverViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication,)

    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        user = self.request.user
        return Driver.objects.filter(user=user)
