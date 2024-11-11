from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from api.models import Ingredient, DislikedIngredients, UserNutrientPreferences

User = get_user_model()



# class JWTTestCase(APITestCase):
#     def setUp(self):
#         # Set up user data and create a test user
#         self.user_data = {
#             'email': 'test@example.com',
#             'password': 'password123',
#             'name': 'Test',
#             'surname': 'User'
#         }
#         self.user = User.objects.create_user(**self.user_data)
        
#         # Set the URL for token endpoint
#         self.url = '/api/token/'  # Adjust this if your token endpoint is different
        
#     def test_jwt_token_obtain_pair(self):
#         """
#         Test obtaining JWT access and refresh tokens using valid credentials.
#         """
#         response = self.client.post('/api/token/', self.user_data, format='json')
        
#         # Check if status code is 200 (OK)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
        
#         # Check if access and refresh tokens are returned
#         self.assertIn('access', response.data)
#         self.assertIn('refresh', response.data)

#         # Store the tokens for later use
#         self.access_token = response.data['access']
#         self.refresh_token = response.data['refresh']

#     def test_jwt_token_refresh(self):
#         """
#         Test refreshing the access token using the refresh token.
#         """
#         # First, obtain the token pair
#         response = self.client.post('/api/token/', self.user_data, format='json')
#         refresh_token = response.data['refresh']

#         # Use the refresh token to get a new access token
#         refresh_response = self.client.post('/api/token/refresh/', {'refresh': refresh_token}, format='json')
        
#         # Check if status code is 200 (OK)
#         self.assertEqual(refresh_response.status_code, status.HTTP_200_OK)
        
#         # Ensure that a new access token is returned
#         self.assertIn('access', refresh_response.data)

#         # Check that the new access token is different from the old one
#         self.assertNotEqual(refresh_response.data['access'], response.data['access'])

#     def test_protected_view_with_token(self):
#         """
#         Test accessing a protected view using the access token.
#         """
#         # Obtain token pair
#         response = self.client.post(self.url, self.user_data, format='json')

#         # Ensure that the response contains access and refresh tokens
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         access_token = response.data.get('access')
#         self.assertIsNotNone(access_token)  # Ensure that the access token is present

#         # Set the credentials for future requests to include the access token
#         self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

#         # Access protected view using the token
#         protected_url = '/api/protected/'  # Ensure this matches your actual protected URL
#         protected_response = self.client.get(protected_url)

#         # Check for status code 200 OK
#         self.assertEqual(protected_response.status_code, status.HTTP_200_OK)

#         # Clear credentials after the test
#         self.client.credentials()
   
#     def test_access_protected_view_without_token(self):
#         """
#         Test trying to access a protected view without a token.
#         """
#         protected_url = '/api/protected/'  # Replace with your actual protected view URL
        
#         response = self.client.get(protected_url)
        
#         # Expecting a 401 Unauthorized error since no token is provided
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)



class EndpointsTestCase(APITestCase):
    def setUp(self):
        # Set up user data and create a test user
        self.user_data = {
            'email': 'test@example.com',
            'password': 'password123',
            'name': 'Test',
            'surname': 'User'
        }
        self.user = User.objects.create_user(**self.user_data)
        
        # Create ingredients for testing
        self.ingredient1 = Ingredient.objects.create(name="Tomato")
        self.ingredient2 = Ingredient.objects.create(name="Onion")

        # Authenticate the user
        self.client.force_authenticate(user=self.user)

    def test_set_user_nutrient_preferences(self):
        """
        Test setting the nutrient preferences for the user.
        """
        url = '/api/preferences/'  # Direct URL for nutrient preferences
        data = {
            "min_calories": 100,
            "max_calories": 200,
            "min_sugars": 10,
            "max_sugars": 20,
            "min_protein": 15,
            "max_protein": 30,
            "min_iron": 5,
            "max_iron": 10,
            "min_potassium": 200,
            "max_potassium": 400
        }

        response = self.client.post(url, data, format='json')

        # Check if the status code is 200 and preferences were correctly set
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the response contains the expected fields
        self.assertEqual(response.data['min_calories'], 100)
        self.assertEqual(response.data['max_calories'], 200)
        self.assertEqual(response.data['min_sugars'], 10)
        self.assertEqual(response.data['max_sugars'], 20)
        self.assertEqual(response.data['min_protein'], 15)
        self.assertEqual(response.data['max_protein'], 30)
        self.assertEqual(response.data['min_iron'], 5)
        self.assertEqual(response.data['max_iron'], 10)
        self.assertEqual(response.data['min_potassium'], 200)
        self.assertEqual(response.data['max_potassium'], 400)

    def test_set_user_nutrient_preferences_with_negative_values(self):
        """
        Test setting the nutrient preferences with negative values.
        """
        url = '/api/preferences/'  # Direct URL for nutrient preferences
        data = {
            "min_calories": -100,
            "max_calories": -200,
            "min_sugars": -10,
            "max_sugars": -20,
            "min_protein": -15,
            "max_protein": -30,
            "min_iron": -5,
            "max_iron": -10,
            "min_potassium": -200,
            "max_potassium": -400
        }

        response = self.client.post(url, data, format='json')

        # Expect a 400 error due to invalid (negative) values
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check that the response contains specific validation errors
        self.assertIn('min_calories', response.data)
        self.assertIn('max_calories', response.data)
        self.assertIn('min_sugars', response.data)
        self.assertIn('max_sugars', response.data)

    def test_set_user_nutrient_preferences_with_letters(self):
        """
        Test setting the nutrient preferences with non-numeric values (letters).
        """
        url = '/api/preferences/'  # Direct URL for nutrient preferences
        data = {
            "min_calories": "abc",
            "max_calories": "xyz",
            "min_sugars": "def",
            "max_sugars": "ghi",
            "min_protein": "jkl",
            "max_protein": "mno",
            "min_iron": "pqr",
            "max_iron": "stu",
            "min_potassium": "vwx",
            "max_potassium": "yz"
        }

        response = self.client.post(url, data, format='json')

        # Expect a 400 error due to invalid (non-numeric) values
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check that the response contains specific validation errors
        self.assertIn('min_calories', response.data)
        self.assertIn('max_calories', response.data)
        self.assertIn('min_sugars', response.data)
        self.assertIn('max_sugars', response.data)

    def test_set_user_nutrient_preferences_with_missing_fields(self):
        """
        Test setting the nutrient preferences with missing fields.
        """
        url = '/api/preferences/'  # Direct URL for nutrient preferences
        data = {
            "min_calories": 100,
            "max_calories": 200,
            "min_sugars": 10,
            # Missing max_sugars, min_protein, max_protein, etc.
        }

        response = self.client.post(url, data, format='json')

        # Expect a 400 error due to missing fields
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_user_nutrient_preferences(self):
        """
        Test retrieving the user's nutrient preferences.
        """
        # First, set the preferences
        self.test_set_user_nutrient_preferences()

        # Get the preferences for the user
        url = '/api/preferences/'  # Direct URL for nutrient preferences
        response = self.client.get(url)

        # Check if the response is correct
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['min_calories'], 100)

    def test_post_user_disliked_ingredients(self):
        """
        Test posting disliked ingredients for the user.
        """
        url = '/api/disliked-ingredients/'  # Direct URL for disliked ingredients endpoint
        data = {"ingredient_ids": [self.ingredient1.id, self.ingredient2.id]}
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["message"], "Disliked ingredients saved successfully.")
        
        # Verify that the disliked ingredients are saved in the database
        self.assertTrue(DislikedIngredients.objects.filter(user=self.user, ingredient=self.ingredient1).exists())
        self.assertTrue(DislikedIngredients.objects.filter(user=self.user, ingredient=self.ingredient2).exists())

    def test_post_user_disliked_ingredients_with_invalid_id(self):
        """
        Test posting disliked ingredients with an invalid (non-existent) ingredient ID.
        """
        url = '/api/disliked-ingredients/'  # Direct URL for disliked ingredients endpoint

        # Use an invalid ingredient ID (e.g., a very large number or a non-existent ID)
        invalid_ingredient_id = 99999999  # Assuming this ID does not exist in the database
        data = {"ingredient_ids": [invalid_ingredient_id]}
        
        response = self.client.post(url, data, format='json')

        # Expect a 400 error due to invalid ingredient ID
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check that the response contains an error related to the invalid ingredient ID
        self.assertIn('ingredient_ids', response.data)  # Ensure 'ingredient_ids' is in the error message
        self.assertIn(f"Invalid ingredient id(s): {invalid_ingredient_id}", str(response.data))


    def test_get_user_disliked_ingredients(self):
        """
        Test retrieving disliked ingredients for the user.
        """
        # Pre-populate disliked ingredients for the user
        DislikedIngredients.objects.create(user=self.user, ingredient=self.ingredient1)
        DislikedIngredients.objects.create(user=self.user, ingredient=self.ingredient2)

        url = '/api/disliked-ingredients/'  # Direct URL for disliked ingredients endpoint
        response = self.client.get(url)

        # Ensure the disliked ingredients are returned
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ingredient_names = [item["name"] for item in response.data]
        self.assertIn(self.ingredient1.name, ingredient_names)
        self.assertIn(self.ingredient2.name, ingredient_names)
