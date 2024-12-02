from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from api.models import (Ingredient, DislikedIngredients, UserNutrientPreferences, RecipeIngredients, UserWeight,
                        Cart, CartIngredient
                        )
from datetime import timedelta
from django.utils.timezone import now

User = get_user_model()



class JWTTestCase(APITestCase):
    def setUp(self):
        # Set up user data and create a test user
        self.user_data = {
            'email': 'test@example.com',
            'password': 'password123',
            'name': 'Test',
            'surname': 'User'
        }
        self.user = User.objects.create_user(**self.user_data)
        
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

class UserWeightTestCase(APITestCase):
    def setUp(self):
        # Create a test user
        self.user_data = {
            'email': 'testuser@example.com',
            'password': 'securepassword123',
            'name': 'John',
            'surname': 'Doe'
        }
        self.user = User.objects.create_user(**self.user_data)

        # Authenticate the test user and obtain a token
        self.url = '/api/can-update-weight/'  # Replace with the actual endpoint
        self.client.force_authenticate(user=self.user)

        # Create a weight entry for the current week
        today = now().date()
        start_of_week = today - timedelta(days=today.weekday())
        self.weekly_weight_entry = UserWeight.objects.create(
            user=self.user,
            weight="70",
            date=start_of_week
        )

    def test_can_update_weight_true(self):
        """
        Test that the endpoint returns true when the user has not logged weight for the current week.
        """
        # Delete existing weight entry to test the case where the user can update
        self.weekly_weight_entry.delete()

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['can_update'])

    def test_can_update_weight_false(self):
        """
        Test that the endpoint returns false when the user has already logged weight for the current week.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['can_update'])

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


    # def test_get_user_disliked_ingredients(self):
    #     """
    #     Test retrieving disliked ingredients for the user.
    #     """
    #     # Pre-populate disliked ingredients for the user
    #     DislikedIngredients.objects.create(user=self.user, ingredient=self.ingredient1)
    #     DislikedIngredients.objects.create(user=self.user, ingredient=self.ingredient2)

    #     url = '/api/disliked-ingredients/'  # Direct URL for disliked ingredients endpoint
    #     response = self.client.get(url)

    #     # Ensure the disliked ingredients are returned
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     ingredient_names = [item["name"] for item in response.data]
    #     self.assertIn(self.ingredient1.name, ingredient_names)
    #     self.assertIn(self.ingredient2.name, ingredient_names)

from django.test import TestCase
from api.models import Recipe, Ingredient, DislikedIngredients, User
from api.utils import select_meals  # Import the `select_meals` function
from django.contrib.auth import get_user_model

class SelectMealsTests(TestCase):
    def setUp(self):
        # Create a test user and set their nutrient preferences
        self.user = get_user_model().objects.create_user(email='test@example.com', password='testpass')
        self.user.nutrient_preferences = {
            'min_calories': 200,
            'max_calories': 3000,
            'min_sugars': 5,
            'max_sugars': 50,
            'min_protein': 10,
            'max_protein': 200,
            'min_iron': 5,
            'max_iron': 20,
            'min_potassium': 1000,
            'max_potassium': 4000,
        }
        self.user.save()
        
        self.recipe1 = Recipe.objects.create(
            title="Test Recipe",
            description="A recipe with a disliked ingredient.",
            total_calories=300,
            sugars=10,
            protein=15,
            iron=2,
            potassium=500,
            preparation_time=20,
            preparation_guide="Mix ingredients and cook.",
            meal_type="main"
        )
        # Create some ingredients
        self.ingredient1 = Ingredient.objects.create(name="Tomato")
        self.ingredient2 = Ingredient.objects.create(name="Chicken")
        self.ingredient3 = Ingredient.objects.create(name="Salt")
    
        # Create a relationship between recipe1 and ingredient1
        RecipeIngredients.objects.create(recipe=self.recipe1, ingredient=self.ingredient1)

        # Add the disliked ingredient to the user's disliked ingredients list
        DislikedIngredients.objects.create(user=self.user, ingredient=self.ingredient1)
        
        
        # Create recipes with varied nutritional values
        Recipe.objects.create(
            title="Vegetable Stir Fry",
            description="A quick and healthy stir fry with mixed vegetables.",
            total_calories="350", 
            sugars="1", 
            protein="8", 
            iron="4", 
            potassium="600", 
            preparation_time=20,
            preparation_guide="Stir-fry the vegetables in olive oil for 10 minutes.",
            meal_type="main"
        )

        Recipe.objects.create(
            title="Chicken Caesar Salad",
            description="A classic Caesar salad with grilled chicken.",
            total_calories="500", 
            sugars="3", 
            protein="35", 
            iron="2", 
            potassium="800", 
            preparation_time=15,
            preparation_guide="Grill the chicken, toss with lettuce, croutons, and Caesar dressing.",
            meal_type="main"
        )

        Recipe.objects.create(
            title="Spaghetti Bolognese",
            description="A rich pasta dish with a savory Bolognese sauce.",
            total_calories="600", 
            sugars="5", 
            protein="25", 
            iron="3", 
            potassium="750", 
            preparation_time=40,
            preparation_guide="Cook the spaghetti and simmer the Bolognese sauce for 30 minutes.",
            meal_type="main"
        )

        Recipe.objects.create(
            title="Vegan Buddha Bowl",
            description="A hearty vegan bowl with quinoa, roasted veggies, and avocado.",
            total_calories="450", 
            sugars="2", 
            protein="15", 
            iron="5", 
            potassium="900", 
            preparation_time=30,
            preparation_guide="Roast the vegetables, cook the quinoa, and assemble with avocado.",
            meal_type="main"
        )

        Recipe.objects.create(
            title="Greek Yogurt Parfait",
            description="A refreshing yogurt parfait with berries and granola.",
            total_calories="200", 
            sugars="10", 
            protein="10", 
            iron="1", 
            potassium="300", 
            preparation_time=10,
            preparation_guide="Layer Greek yogurt with fresh berries and granola.",
            meal_type="snack"
        )

        Recipe.objects.create(
            title="Eggplant Parmesan",
            description="A delicious vegetarian dish with breaded eggplant and marinara sauce.",
            total_calories="400", 
            sugars="10", 
            protein="20", 
            iron="4", 
            potassium="600", 
            preparation_time=50,
            preparation_guide="Bread the eggplant slices, fry, and bake with marinara sauce and cheese.",
            meal_type="main"
        )

        Recipe.objects.create(
            title="Beef Tacos",
            description="Spicy beef tacos with fresh toppings.",
            total_calories="450", 
            sugars="5", 
            protein="25", 
            iron="6", 
            potassium="500", 
            preparation_time=25,
            preparation_guide="Cook the beef with taco seasoning, then assemble with tortillas and toppings.",
            meal_type="main"
        )

        Recipe.objects.create(
            title="Mango Smoothie",
            description="A refreshing smoothie made with ripe mango and coconut milk.",
            total_calories="250", 
            sugars="11", 
            protein="2", 
            iron="1", 
            potassium="400", 
            preparation_time=5,
            preparation_guide="Blend mango and coconut milk until smooth.",
            meal_type="beverage"
        )

        Recipe.objects.create(
            title="Pancakes",
            description="Fluffy pancakes topped with maple syrup and berries.",
            total_calories="350", 
            sugars="1", 
            protein="8", 
            iron="3", 
            potassium="400", 
            preparation_time=20,
            preparation_guide="Mix the ingredients, cook pancakes, and serve with syrup.",
            meal_type="breakfast"
        )

        Recipe.objects.create(
            title="Chicken Stir Fry with Rice",
            description="A delicious stir fry with chicken, vegetables, and rice.",
            total_calories="550", 
            sugars="10", 
            protein="30", 
            iron="3", 
            potassium="700", 
            preparation_time=30,
            preparation_guide="Stir fry chicken and vegetables, then serve with cooked rice.",
            meal_type="main"
)

    def test_basic_selection(self):
        """Test if basic selection works without any disliked ingredients or constraints."""
        selected_meals = select_meals(optimize_field='protein', objective='maximize', user=self.user)

        # Check that some meals were selected
        self.assertTrue(len(selected_meals) > 0, "Expected meals to be selected")

   
    # def test_disliked_ingredient_exclusion(self):
    #     """Test that recipes containing a disliked ingredient are excluded from meal selection."""

    #     # Add disliked ingredient via the through model
    #     disliked_ingredient = Ingredient.objects.create(name="Onion")
    #     DislikedIngredients.objects.create(user=self.user, ingredient=disliked_ingredient)

    #     # Create recipes
    #     recipe_with_disliked_ingredient = Recipe.objects.create(
    #         title="Onion Soup",
    #         description="Soup made with onions",
    #         total_calories="150",
    #         sugars="5",
    #         protein="2",
    #         iron="1",
    #         potassium="10",
    #         preparation_time=30,
    #         preparation_guide="Boil onions and season",
    #         meal_type="Lunch"
    #     )
    #     RecipeIngredients.objects.create(
    #         recipe=recipe_with_disliked_ingredient,
    #         ingredient=disliked_ingredient,
    #         quantity=1,
    #         unit="piece"
    #     )

    #     recipe_without_disliked_ingredient = Recipe.objects.create(
    #         title="Tomato Salad",
    #         description="Fresh tomato salad",
    #         total_calories="100",
    #         sugars="4",
    #         protein="1",
    #         iron="0.5",
    #         potassium="8",
    #         preparation_time=15,
    #         preparation_guide="Mix sliced tomatoes with dressing",
    #         meal_type="Dinner"
    #     )
    #     tomato = Ingredient.objects.create(name="Tomato")
    #     RecipeIngredients.objects.create(
    #         recipe=recipe_without_disliked_ingredient,
    #         ingredient=tomato,
    #         quantity=2,
    #         unit="pieces"
    #     )

    #     # Run the meal selection logic
    #     selected_meals = select_meals(self.user)

    #     # Assert that recipes with disliked ingredients are excluded
    #     self.assertNotIn(recipe_with_disliked_ingredient, selected_meals,
    #                     "Recipe with disliked ingredient should not be selected.")
    #     # Assert that recipes without disliked ingredients are included
    #     self.assertIn(recipe_without_disliked_ingredient, selected_meals,
    #                 "Recipe without disliked ingredients should be selected.")


    def test_nutritional_preferences_constraints(self):
        """Test that selected meals respect the user's nutritional preferences."""
        selected_meals = select_meals(optimize_field='protein', objective='maximize', user=self.user)

        # Calculate total nutritional values of the selected meals
        total_calories = sum(int(meal.total_calories) for meal in selected_meals)  
        total_sugars = sum(int(meal.sugars) for meal in selected_meals)            
        total_protein = sum(int(meal.protein) for meal in selected_meals)          
        total_iron = sum(int(meal.iron) for meal in selected_meals)                
        total_potassium = sum(int(meal.potassium) for meal in selected_meals)

        # Check if totals are within user's preferred ranges
        self.assertGreaterEqual(total_calories, self.user.nutrient_preferences['min_calories'])
        self.assertLessEqual(total_calories, self.user.nutrient_preferences['max_calories'])
        self.assertGreaterEqual(total_sugars, self.user.nutrient_preferences['min_sugars'])
        self.assertLessEqual(total_sugars, self.user.nutrient_preferences['max_sugars'])
        self.assertGreaterEqual(total_protein, self.user.nutrient_preferences['min_protein'])
        self.assertLessEqual(total_protein, self.user.nutrient_preferences['max_protein'])
        self.assertGreaterEqual(total_iron, self.user.nutrient_preferences['min_iron'])
        self.assertLessEqual(total_iron, self.user.nutrient_preferences['max_iron'])
        self.assertGreaterEqual(total_potassium, self.user.nutrient_preferences['min_potassium'])
        self.assertLessEqual(total_potassium, self.user.nutrient_preferences['max_potassium'])
        
    def test_meal_type_coverage(self):
        """Test that at least one meal from each meal type is included."""
        selected_meals = select_meals(optimize_field='protein', objective='maximize', user=self.user)
        meal_types = [meal.meal_type for meal in selected_meals]

        # Check that each required meal type is represented at least once
        for meal_type in ['lunch', 'dinner', 'snack', 'breakfast']:
            if Recipe.objects.filter(meal_type=meal_type).exists():
                self.assertIn(meal_type, meal_types, f"Expected at least one {meal_type} in selection")
                
class CartTestCase(APITestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(email="test@example.com", password="password123")
        self.client.login(email="test@example.com", password="password123")
        self.cart = Cart.objects.create(user=self.user)
        self.ingredient = Ingredient.objects.create(name="Flour")
        self.cart_ingredient = CartIngredient.objects.create(
            cart=self.cart,
            ingredient=self.ingredient,
            quantity=2,
            unit="cups"
        )

    def test_update_quantity(self):
        response = self.client.patch(f'/api/cart/{self.cart_ingredient.id}/', {'quantity': 5})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.cart_ingredient.refresh_from_db()
        self.assertEqual(self.cart_ingredient.quantity, 5)

    def test_remove_ingredient(self):
        response = self.client.delete(f'/api/cart/{self.cart_ingredient.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        with self.assertRaises(CartIngredient.DoesNotExist):
            self.cart_ingredient.refresh_from_db()

    def test_clear_cart(self):
        response = self.client.delete('/api/cart/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(CartIngredient.objects.count(), 0)