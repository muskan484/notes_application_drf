from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User

class UserAPITestCase(TestCase):
    def setUp(self):
        """
        Set up the test case by creating a test client.
        """
        self.client = APIClient()

    def test_user_signup(self):
        """
        Checks if a user can successfully sign up and if the response status code is 201.
        """
        self.url = reverse('user-signup')
        data = {'username': 'test01', 'password': 'test01password','email':'test01@gmail.com'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'test01')

    def test_user_login(self):
        """
        Verifies if a user can log in with valid credentials and if the response status code is 200.
        """
        user = User.objects.create_user(username='test01', password='test01password')
        url = reverse('user-login')
        data = {'username': 'test01', 'password': 'test01password'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Access_token', response.data)

    def test_invalid_user_login(self):
        """
        Checks if the user login fails with invalid credentials and if the response status code is 404.
        """
        url = reverse('user-login')
        data = {'username': 'nonexistentuser', 'password': 'invalidpassword'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["Message"], "User not found")

