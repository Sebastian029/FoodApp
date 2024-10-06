from django.test import TestCase
from django.urls import reverse

class WelcomeEndpointTest(TestCase):
    def test_welcome_endpoint(self):
        response = self.client.get(reverse('welcome'))  # Use the URL name defined in urls.py
        self.assertEqual(response.status_code, 200)  # Check for a 200 OK response
        self.assertEqual(response.json(), {"message": "Welcome to the Django API!"})  # Check response data
