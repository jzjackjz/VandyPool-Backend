from rest_framework.test import APITestCase
from rest_framework import status
from api.models import Timeslot, FlightInformation, Driver
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class TimeslotViewSetTestCase(APITestCase):
    def setUp(self):
        self.timeslot1 = Timeslot.objects.create(
            user='JohnDoe',
            date='2023-01-01',
            time='12:00:00',
            space_available=5
        )
        self.timeslot2 = Timeslot.objects.create(
            user='JohnDoe',
            date='2023-01-02',
            time='14:00:00',
            space_available=3
        )

    def test_list_all_timeslots(self):
        response = self.client.get('/timeslot/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_list_user_timeslots(self):
        response = self.client.get('/timeslot/', {'username': 'JohnDoe'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_list_user_timeslots_invalid_username(self):
        response = self.client.get('/timeslot/', {'username': 'InvalidUser'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_create_timeslot(self):
        data = {
            'user': 'JohnDoe',
            'date': '2023-01-03',
            'time': '16:30:00',
            'space_available': 8,
        }
        response = self.client.post('/timeslot/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Timeslot.objects.count(), 3) 

    def test_retrieve_timeslot(self):
        response = self.client.get(f'/timeslot/{self.timeslot1.id}/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['space_available'], 5)

    def test_update_timeslot(self):
        data = {
            'user': 'JohnDoe',
            'date': '2023-01-01',
            'time': '14:00:00',
            'space_available': 7,
        }
        response = self.client.put(f'/timeslot/{self.timeslot1.id}/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['time'], '14:00:00')
        self.timeslot1.refresh_from_db()

    def test_delete_timeslot(self):
        response = self.client.delete(f'/timeslot/{self.timeslot2.id}/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Timeslot.objects.count(), 1)

class FlightInformationViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='JohnDoe', password='password123')
        self.token = Token.objects.create(user=self.user)

        self.flight_info = FlightInformation.objects.create(
            user=self.user,
            ride_type='One-way',
            flight_time='12:00:00',
            flight_date='2023-01-01',
            dropoff_point='Airport',
            airline='AirlineX',
        )

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

    def test_create_flight_information(self):
        data = {
            'ride_type': 'Round-trip',
            'flight_time': '14:00:00',
            'flight_date': '2023-02-01',
            'dropoff_point': 'City Center',
            'airline': 'AirlineY',
        }
        response = self.client.post('/flights/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(FlightInformation.objects.count(), 2)  

    def test_retrieve_flight_information(self):
        response = self.client.get(f'/flights/{self.flight_info.id}/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['ride_type'], 'One-way')

    def test_update_flight_information(self):
        data = {
            'ride_type': 'One-way',
            'flight_time': '15:30:00',
            'flight_date': '2023-01-01',
            'dropoff_point': 'City Center',
            'airline': 'UpdatedAirline',
        }
        response = self.client.put(f'/flights/{self.flight_info.id}/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['airline'], 'UpdatedAirline')
        self.flight_info.refresh_from_db()
        self.assertEqual(self.flight_info.airline, 'UpdatedAirline')

    def test_delete_flight_information(self):
        response = self.client.delete(f'/flights/{self.flight_info.id}/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(FlightInformation.objects.count(), 0)

    def test_list_flight_information(self):
        response = self.client.get('/flights/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  

class DriverViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='JohnDoe', password='password123')
        self.token = Token.objects.create(user=self.user)

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

    def test_create_driver(self):
        data = {
            'carModel': 'Tesla',
            'carColor': 'Black',
            'licensePlate': 'ABC123',
        }
        response = self.client.post('/driver/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Driver.objects.count(), 1)

    def test_retrieve_driver(self):
        driver = Driver.objects.create(
            user=self.user,
            carModel='Tesla',
            carColor='Black',
            licensePlate='ABC123',
        )
        response = self.client.get(f'/driver/{driver.id}/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['carModel'], 'Tesla')

    def test_update_driver(self):
        driver = Driver.objects.create(
            user=self.user,
            carModel='Tesla',
            carColor='Black',
            licensePlate='ABC123',
        )
        data = {
            'carModel': 'BMW',
            'carColor': 'White',
            'licensePlate': 'XYZ456',
        }
        response = self.client.put(f'/driver/{driver.id}/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['carModel'], 'BMW')
        driver.refresh_from_db()
        self.assertEqual(driver.carModel, 'BMW')

    def test_delete_driver(self):
        driver = Driver.objects.create(
            user=self.user,
            carModel='Tesla',
            carColor='Black',
            licensePlate='ABC123',
        )
        response = self.client.delete(f'/driver/{driver.id}/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Driver.objects.count(), 0)

    def test_list_drivers(self):
        response = self.client.get('/driver/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)  # Assuming no records exist initially