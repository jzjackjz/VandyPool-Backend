from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.authtoken.models import Token
from api.models import FlightInformation
from api.serializers import FlightInformationSerializer
from rest_framework.test import APIRequestFactory


class FlightInformationSerializerTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='JohnDoe', password='password123')
        self.token = Token.objects.create(user=self.user)
        self.factory = APIRequestFactory()

    def test_flight_information_serializer_valid_data(self):
        data = {
            'ride_type': 'One-way',
            'flight_time': '12:00:00',
            'flight_date': '2023-01-01',
            'dropoff_point': 'Airport',
            'airline': 'AirlineX',
        }

        request = self.factory.post('/flights/', data, format='json')
        request.user = self.user

        serializer = FlightInformationSerializer(data=data, context={'request': request})

        self.assertTrue(serializer.is_valid())
        instance = serializer.save()

        self.assertEqual(instance.user, self.user)
        self.assertEqual(FlightInformation.objects.count(), 1)
