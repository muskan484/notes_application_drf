from .models import Note
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User

class NoteViewsTestCase(TestCase):
    def setUp(self):
        """
        Set up method to prepare the test environment.
        This method is called before each test method to set up the necessary
        objects and configurations for testing.
        """
        self.client = APIClient()
        self.user = User.objects.create_user(username="test01", password="test01password",email="test01@gmail.com")
        self.user2 = User.objects.create_user(username='test02', password='test02password',email="test02@gmail.com")
        self.note = Note.objects.create(content='Test note content', owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_create_note_view(self):
        """
        This method tests the functionality to create a new note by sending
        a POST request to the appropriate endpoint. It checks whether the
        response status code indicates a successful creation (HTTP 201 Created).
        """
        url = reverse("create-note")
        data = {"content": "Test note content"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_update_delete_note_view(self):
        """
        This method tests the functionality to retrieve, update, and delete
        a note by sending GET, PUT, and DELETE requests to the appropriate
        endpoints, respectively. It checks whether the response status codes
        indicate successful operations (HTTP 200 OK, HTTP 204 No Content).
        """
        url = reverse('retrieve-update-delete-note', kwargs={'id': self.note.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = {'content': 'Updated test note content'}
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_share_note_view(self):
        """
        This method tests the functionality to share a note with another user
        by sending a POST request to the appropriate endpoint. It checks whether
        the response status code indicates a successful operation (HTTP 200 OK).
        """
        url = reverse('share-note')
        data = {'note_id': self.note.id, 'shared_users': ['test02']}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_note_version_history_view(self):
        """
        This method tests the functionality to retrieve the version history
        of a note by sending a GET request to the appropriate endpoint. It
        checks whether the response status code indicates a successful operation
        (HTTP 200 OK).
        """
        url = reverse('note-version-history', kwargs={'id': self.note.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
