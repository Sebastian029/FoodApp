from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

class JWTTestCase(APITestCase):
    def setUp(self):
        # Set up user data and create a test user
        self.user_data = {
            'email': 'test@example.com',
            'password': 'password123',
            'name': 'Test',
            'surname': 'User'
        }
        self.user = get_user_model().objects.create_user(**self.user_data)
        
        # Set the URL for token endpoint
        self.url = '/api/token/'  # Adjust this if your token endpoint is different
        
    def test_jwt_token_obtain_pair(self):
        """
        Test obtaining JWT access and refresh tokens using valid credentials.
        """
        response = self.client.post('/api/token/', self.user_data, format='json')
        
        # Check if status code is 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check if access and refresh tokens are returned
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

        # Store the tokens for later use
        self.access_token = response.data['access']
        self.refresh_token = response.data['refresh']

    def test_jwt_token_refresh(self):
        """
        Test refreshing the access token using the refresh token.
        """
        # First, obtain the token pair
        response = self.client.post('/api/token/', self.user_data, format='json')
        refresh_token = response.data['refresh']

        # Use the refresh token to get a new access token
        refresh_response = self.client.post('/api/token/refresh/', {'refresh': refresh_token}, format='json')
        
        # Check if status code is 200 (OK)
        self.assertEqual(refresh_response.status_code, status.HTTP_200_OK)
        
        # Ensure that a new access token is returned
        self.assertIn('access', refresh_response.data)

        # Check that the new access token is different from the old one
        self.assertNotEqual(refresh_response.data['access'], response.data['access'])

    def test_protected_view_with_token(self):
        """
        Test accessing a protected view using the access token.
        """
        # Obtain token pair
        response = self.client.post(self.url, self.user_data, format='json')

        # Ensure that the response contains access and refresh tokens
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        access_token = response.data.get('access')
        self.assertIsNotNone(access_token)  # Ensure that the access token is present

        # Set the credentials for future requests to include the access token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # Access protected view using the token
        protected_url = '/api/protected/'  # Ensure this matches your actual protected URL
        protected_response = self.client.get(protected_url)

        # Check for status code 200 OK
        self.assertEqual(protected_response.status_code, status.HTTP_200_OK)

        # Clear credentials after the test
        self.client.credentials()
   
    def test_access_protected_view_without_token(self):
        """
        Test trying to access a protected view without a token.
        """
        protected_url = '/api/protected/'  # Replace with your actual protected view URL
        
        response = self.client.get(protected_url)
        
        # Expecting a 401 Unauthorized error since no token is provided
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
