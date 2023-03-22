from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model


User = get_user_model()

class UserRegistrationTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_valid_registration(self):
        user_data = {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'testuser@example.com',
            'password': 'testpassword',
        }

        response = self.client.post(reverse('user-registration'), user_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_duplicate_username_registration(self):
        existing_user = User.objects.create_user(
            username='existinguser',
            first_name='Existing',
            last_name='User',
            email='existinguser@example.com',
            password='existingpassword',
        )
        user_data = {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'existinguser@example.com',
            'password': 'testpassword',
        }

        response = self.client.post(reverse('user-registration'), user_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(User.objects.filter(username='testuser').exists())
        
    def test_duplicate_email_registration(self):
        existing_user = User.objects.create_user(
            username='existinguser',
            first_name='Existing',
            last_name='User',
            email='existinguser@example.com',
            password='existingpassword',
        )
        user_data = {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'existinguser@example.com',
            'password': 'testpassword',
        }

        response = self.client.post(reverse('user-registration'), user_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(User.objects.filter(username='testuser').exists())