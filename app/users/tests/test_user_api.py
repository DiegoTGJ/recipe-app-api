
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse


from rest_framework import status
from rest_framework.test import APIClient


CREATE_USER_URL = reverse('users:create')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


def PublicUserApiTest(TestCase):
    """Test the user API (public)"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_succes(self):
        """Test creating user with valid payload is succesful"""
        payload = {
            'email': 'test@test.test',
            'password': 'test',
            'name': 'Test name'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """Test creating a duplicate user fails"""
        payload = {
            'name': 'holi',
            'email': 'test@test.test',
            'password': 'test',
        }
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test that the password must be more than 5 characters"""
        payload = {
            'email': 'test@test.test',
            'password': 'G121asd',
            'name': 'prueba',
        }
        res = self.client.post(CREATE_USER_URL, payload)
        print(f'holi {res}')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)