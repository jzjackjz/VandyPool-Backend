from django.test import TestCase
from django.contrib.auth.models import User
from api.models import UserProfile, FlightInformation, Timeslot, Driver
from datetime import time, date


class UserProfileModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='JohnDoe', password='password123')
        self.user_profile = UserProfile.objects.create(
            user=self.user,
            google_id='google_id_123',
            phone_number='1234567890',
            profile_picture_url='https://example.com/johndoe.jpg',
        )

    def test_user_profile_creation(self):
        self.assertEqual(UserProfile.objects.count(), 1)

    def test_user_profile_fields(self):
        user_profile = UserProfile.objects.get(google_id='google_id_123')
        self.assertEqual(user_profile.user, self.user)
        self.assertEqual(user_profile.phone_number, '1234567890')
        self.assertEqual(user_profile.profile_picture_url, 'https://example.com/johndoe.jpg')

    def test_google_id_unique(self):
        with self.assertRaises(Exception):
            UserProfile.objects.create(
                user=User.objects.create_user(username='JaneDoe', password='password456'),
                google_id='google_id_123',  
                phone_number='9876543210',
                profile_picture_url='https://example.com/janedoe.jpg',
            )

class FlightInformationModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='JohnDoe', password='password123')
        self.flight_info = FlightInformation.objects.create(
            user=self.user,
            ride_type='One-way',
            flight_time=time(12, 0, 0),
            flight_date=date(2023, 1, 1),
            dropoff_point='Airport',
            airline='AirlineX',
        )

    def test_flight_information_creation(self):
        self.assertEqual(FlightInformation.objects.count(), 1)

    def test_flight_information_fields(self):
        flight_info = FlightInformation.objects.get(ride_type='One-way')
        self.assertEqual(flight_info.user, self.user)
        self.assertEqual(flight_info.flight_time, time(12, 0, 0))
        self.assertEqual(flight_info.flight_date, date(2023, 1, 1))
        self.assertEqual(flight_info.dropoff_point, 'Airport')
        self.assertEqual(flight_info.airline, 'AirlineX')

    def test_string_representation(self):
        self.assertEqual(str(self.flight_info), 'One-way')


class TimeslotModelTestCase(TestCase):
    def setUp(self):
        self.timeslot = Timeslot.objects.create(
            date=date(2023, 1, 1),
            time=time(12, 0, 0),
            space_available=10,
            user='JohnDoe',
        )

    def test_timeslot_creation(self):
        self.assertEqual(Timeslot.objects.count(), 1)

    def test_timeslot_fields(self):
        timeslot = Timeslot.objects.get(date=date(2023, 1, 1))
        self.assertEqual(timeslot.time, time(12, 0, 0))
        self.assertEqual(timeslot.space_available, 10)
        self.assertEqual(timeslot.user, 'JohnDoe')


class DriverModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='JohnDoe', password='password123')
        self.driver = Driver.objects.create(
            user=self.user,
            carModel='Tesla',
            carColor='Black',
            licensePlate='ABC123',
        )

    def test_driver_creation(self):
        self.assertEqual(Driver.objects.count(), 1)

    def test_driver_fields(self):
        driver = Driver.objects.get(user=self.user)
        self.assertEqual(driver.carModel, 'Tesla')
        self.assertEqual(driver.carColor, 'Black')
        self.assertEqual(driver.licensePlate, 'ABC123')