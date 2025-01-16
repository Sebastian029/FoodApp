from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from api.models import (Ingredient, DislikedIngredients, RecipeIngredients, UserWeight,
                        Cart, CartIngredient, DayPlanRecipes, DayPlan, UserNutrientPreferences
                        )
from datetime import timedelta, datetime
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
        self.url = '/api/login/'  # Adjust this if your token endpoint is different
        
    def test_jwt_token_obtain_pair(self):
        """
        Test obtaining JWT access and refresh tokens using valid credentials.
        """
        response = self.client.post('/api/login/', self.user_data, format='json')
        
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
        response = self.client.post('/api/login/', self.user_data, format='json')
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
            "min_calories": 1500,
            "max_calories": 2500,
            "min_sugars": 30,
            "max_sugars": 50,
            "min_protein": 50,
            "max_protein": 100,
            "min_iron": 10,
            "max_iron": 20,
            "min_potassium": 3000,
            "max_potassium": 4000,
            "min_carbohydrates": 200,
            "max_carbohydrates": 300,
            "min_fat": 50,
            "max_fat": 80,
            "min_fiber": 20,
            "max_fiber": 35
        }

        response = self.client.post(url, data, format='json')

        # Check if the status code is 200 and preferences were correctly set
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the response contains the expected fields
        self.assertEqual(response.data['min_calories'], 1500)
        self.assertEqual(response.data['max_calories'], 2500)
        self.assertEqual(response.data['min_sugars'], 30)
        self.assertEqual(response.data['max_sugars'], 50)
        self.assertEqual(response.data['min_protein'], 50)
        self.assertEqual(response.data['max_protein'], 100)
        self.assertEqual(response.data['min_iron'], 10)
        self.assertEqual(response.data['max_iron'], 20)
        self.assertEqual(response.data['min_potassium'], 3000)
        self.assertEqual(response.data['max_potassium'], 4000)
        self.assertEqual(response.data['min_carbohydrates'], 200)
        self.assertEqual(response.data['max_carbohydrates'], 300)
        self.assertEqual(response.data['min_fat'], 50)
        self.assertEqual(response.data['max_fat'], 80)
        self.assertEqual(response.data['min_fiber'], 20)
        self.assertEqual(response.data['max_fiber'], 35)

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
            "max_potassium": -400,
            "min_carbohydrates": -50,
            "max_carbohydrates": -100,
            "min_fat": -10,
            "max_fat": -20,
            "min_fiber": -5,
            "max_fiber": -10
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
            "max_potassium": "yz",
            "min_carbohydrates": "uvw",
            "max_carbohydrates": "xyz",
            "min_fat": "abc",
            "max_fat": "def",
            "min_fiber": "ghi",
            "max_fiber": "jkl"
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
            "min_calories": 1500,
            "max_calories": 2500,
            "min_sugars": 30,
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
        self.assertEqual(response.data['min_calories'], 1500)

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



from django.test import TestCase
from api.models import Recipe, Ingredient, DislikedIngredients, User
from api.utils import select_meals  # Import the `select_meals` function
from django.contrib.auth import get_user_model

class SelectMealsTests(TestCase):
    def setUp(self):
        # Create a test user and set their nutrient preferences
        self.user = get_user_model().objects.create_user(email='test@example.com', password='testpass')
        self.user_nutrient_preferences = UserNutrientPreferences.objects.create(
            user=self.user,
            min_calories=200,
            max_calories=3000,
            min_sugars=5,
            max_sugars=50,
            min_protein=10,
            max_protein=200,
            min_iron=5,
            max_iron=20,
            min_potassium=1000,
            max_potassium=4000,
            min_carbohydrates=1,
            max_carbohydrates=100,
            min_fat=1,
            max_fat=100,
            min_fiber=1,
            max_fiber=100
        )
        
        self.user.save()
        
        self.recipe1 = Recipe.objects.create(
            title="Test Recipe",
            description="A recipe with a disliked ingredient.",
            total_calories=300,
            sugars=10,
            protein=15,
            fat=10,
            carbohydrates=5,
            fiber=2,
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
            fat="10",
            carbohydrates="5",
            fiber="2",
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
            fat="10",
            carbohydrates="5",
            fiber="2",
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
            fat="10",
            carbohydrates="5",
            fiber="2", 
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
            fat="10",
            carbohydrates="5",
            fiber="2", 
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
            fat="10",
            carbohydrates="5",
            fiber="2",
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
            fat="10",
            carbohydrates="5",
            fiber="2", 
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
            fat="10",
            carbohydrates="5",
            fiber="2", 
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
            fat="10",
            carbohydrates="5",
            fiber="2", 
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
            fat="10",
            carbohydrates="5",
            fiber="2", 
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
            fat="10",
            carbohydrates="5",
            fiber="2", 
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

    def test_nutritional_preferences_constraints(self):
        """Test that selected meals respect the user's nutritional preferences."""
        selected_meals = select_meals(optimize_field='protein', objective='maximize', user=self.user)
        user_preferences = UserNutrientPreferences.objects.get(user=self.user)
        
        # Calculate total nutritional values of the selected meals
        total_calories = sum(int(meal.total_calories) for meal in selected_meals)  
        total_sugars = sum(int(meal.sugars) for meal in selected_meals)            
        total_protein = sum(int(meal.protein) for meal in selected_meals)          
        total_iron = sum(int(meal.iron) for meal in selected_meals)                
        total_potassium = sum(int(meal.potassium) for meal in selected_meals)
        total_carbohydrates = sum(int(meal.carbohydrates) for meal in selected_meals)  
        total_fat = sum(int(meal.fat) for meal in selected_meals)                     
        total_fiber = sum(int(meal.fiber) for meal in selected_meals)   

        # Check if totals are within user's preferred ranges
        self.assertGreaterEqual(total_calories, user_preferences.min_calories)
        self.assertLessEqual(total_calories, user_preferences.max_calories)
        self.assertGreaterEqual(total_sugars, user_preferences.min_sugars)
        self.assertLessEqual(total_sugars, user_preferences.max_sugars)
        self.assertGreaterEqual(total_protein, user_preferences.min_protein)
        self.assertLessEqual(total_protein, user_preferences.max_protein)
        self.assertGreaterEqual(total_iron, user_preferences.min_iron)
        self.assertLessEqual(total_iron, user_preferences.max_iron)
        self.assertGreaterEqual(total_potassium, user_preferences.min_potassium)
        self.assertLessEqual(total_potassium, user_preferences.max_potassium)
        self.assertGreaterEqual(total_carbohydrates, user_preferences.min_carbohydrates)
        self.assertLessEqual(total_carbohydrates, user_preferences.max_carbohydrates)
        self.assertGreaterEqual(total_fat, user_preferences.min_fat)
        self.assertLessEqual(total_fat, user_preferences.max_fat)
        self.assertGreaterEqual(total_fiber, user_preferences.min_fiber)
        self.assertLessEqual(total_fiber, user_preferences.max_fiber)
        
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
        self.user_data = {
            'email': 'test@example.com',
            'password': 'password123'
        }
        self.user = User.objects.create_user(**self.user_data)

        # Obtain JWT token pair
        response = self.client.post('/api/login/', self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Ensure the tokens are issued
        self.access_token = response.data['access']

        # Set credentials for authenticated requests
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        # Set up cart, ingredients, and cart ingredients
        self.cart = Cart.objects.create(user=self.user)
        self.ingredient = Ingredient.objects.create(name="Flour")
        self.cart_ingredient = CartIngredient.objects.create(
            cart=self.cart,
            ingredient=self.ingredient,
            quantity=2,
            unit="cups"
        )
        
        self.recipe = Recipe.objects.create(
        title="Pancakes",
        description="Delicious pancakes",
        total_calories=500,
        protein=10,
        sugars=5,
        iron=2,
        potassium=200,
        preparation_time=11,
        preparation_guide="Mix and cook.",
        meal_type="Breakfast"
    )

        # Create ingredients (without quantity and unit)
        self.recipe_ingredient_1 = Ingredient.objects.create(name="Eggs")
        self.recipe_ingredient_2 = Ingredient.objects.create(name="Milk")

        # Create RecipeIngredient instances linking ingredients to the recipe with quantities and units
        RecipeIngredients.objects.create(recipe=self.recipe, ingredient=self.recipe_ingredient_1, quantity=3, unit="units")
        RecipeIngredients.objects.create(recipe=self.recipe, ingredient=self.recipe_ingredient_2, quantity=2, unit="cups")


    def test_update_quantity(self):
        """Test updating the quantity of an ingredient in the cart."""
        response = self.client.patch(
            f'/api/cart/{self.cart_ingredient.id}/', 
            {'quantity': 5},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.cart_ingredient.refresh_from_db()  # Refresh to get the updated value
        self.assertEqual(self.cart_ingredient.quantity, 5)  # Check if the quantity was updated correctly

    def test_remove_ingredient(self):
        """Test removing an ingredient from the cart."""
        response = self.client.delete(f'/api/cart/{self.cart_ingredient.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Ensure that the ingredient is removed from the cart
        with self.assertRaises(CartIngredient.DoesNotExist):
            self.cart_ingredient.refresh_from_db()  # Try to refresh and check if it doesn't exist

    def test_clear_cart(self):
        """Test clearing the entire cart by removing all ingredients."""
        # Add another ingredient to the cart to test clearing functionality
        additional_ingredient = Ingredient.objects.create(name="Sugar")
        CartIngredient.objects.create(
            cart=self.cart,
            ingredient=additional_ingredient,
            quantity=1,
            unit="cups"
        )

        response = self.client.delete('/api/cart/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Ensure that all CartIngredient entries are deleted
        self.assertEqual(CartIngredient.objects.filter(cart=self.cart).count(), 0)

    def test_add_ingredient_to_cart(self):
        """Test adding an ingredient to the cart."""
        ingredient_data = {
            'ingredients': [
                {
                    'ingredient_name': 'Sugar',
                    'quantity': 3,
                    'unit': 'cups'
                }
            ]
        }

        response = self.client.post('/api/cart/', ingredient_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check that the ingredient is in the cart now
        ingredient = Ingredient.objects.get(name="Sugar")
        cart_ingredient = CartIngredient.objects.get(cart=self.cart, ingredient=ingredient)
        self.assertEqual(cart_ingredient.quantity, 3)
        self.assertEqual(cart_ingredient.unit, 'cups')

    def test_add_multiple_ingredients_to_cart(self):
        """Test adding multiple ingredients to the cart."""
        ingredient_data = {
            'ingredients': [
                {'ingredient_name': 'Sugar', 'quantity': 3, 'unit': 'cups'},
                {'ingredient_name': 'Butter', 'quantity': 2, 'unit': 'tbsp'}
            ]
        }

        response = self.client.post('/api/cart/', ingredient_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check that both ingredients are added to the cart
        sugar = Ingredient.objects.get(name="Sugar")
        butter = Ingredient.objects.get(name="Butter")

        cart_ingredient_sugar = CartIngredient.objects.get(cart=self.cart, ingredient=sugar)
        cart_ingredient_butter = CartIngredient.objects.get(cart=self.cart, ingredient=butter)

        self.assertEqual(cart_ingredient_sugar.quantity, 3)
        self.assertEqual(cart_ingredient_butter.quantity, 2)
        self.assertEqual(cart_ingredient_sugar.unit, 'cups')
        self.assertEqual(cart_ingredient_butter.unit, 'tbsp')

    def test_add_ingredients_by_recipe(self):
        """Test adding ingredients from a recipe to the cart."""
        recipe_data = {
            'recipe_id': self.recipe.id
        }

        response = self.client.post('/api/cart/', recipe_data, format='json')


        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check that all ingredients from the recipe are added to the cart
        cart_ingredient_eggs = CartIngredient.objects.get(cart=self.cart, ingredient=self.recipe_ingredient_1)
        cart_ingredient_milk = CartIngredient.objects.get(cart=self.cart, ingredient=self.recipe_ingredient_2)

        self.assertEqual(cart_ingredient_eggs.quantity, 3)
        self.assertEqual(cart_ingredient_milk.quantity, 2)
        self.assertEqual(cart_ingredient_eggs.unit, 'units')  # Assume "units" for this example, change as needed
        self.assertEqual(cart_ingredient_milk.unit, 'cups')  # Assume "cups" for this example, change as needed

    def test_add_invalid_ingredient_quantity(self):
        """Test adding ingredients with negative quantity or invalid input (letters)."""
        # Test negative quantity
        ingredient_data_negative = {
            'ingredients': [
                {
                    'ingredient_name': 'Sugar',
                    'quantity': -3,  # Invalid quantity
                    'unit': 'cups'
                }
            ]
        }

        response_negative = self.client.post('/api/cart/', ingredient_data_negative, format='json')
        self.assertEqual(response_negative.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('message', response_negative.data)
        self.assertEqual(response_negative.data['message'], 'Quantity must be a positive number.')

        # Test invalid quantity (letters)
        ingredient_data_invalid = {
            'ingredients': [
                {
                    'ingredient_name': 'Sugar',
                    'quantity': 'abc',  # Invalid quantity (letters)
                    'unit': 'cups'
                }
            ]
        }

        response_invalid = self.client.post('/api/cart/', ingredient_data_invalid, format='json')
        self.assertEqual(response_invalid.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('message', response_invalid.data)
        self.assertEqual(response_invalid.data['message'], 'Quantity must be a positive number.')
        
        
class DayPlanRecipesTests(APITestCase):
    def setUp(self):
        # Create a test user
        self.user_data = {
            'email': 'test@example.com',
            'password': 'password123',
            'name': 'John',
            'surname': 'Doe'
        }
        self.user = User.objects.create_user(**self.user_data)
        self.user_nutrient_preferences = UserNutrientPreferences.objects.create(
            user=self.user,
            min_calories=200,
            max_calories=3000,
            min_sugars=5,
            max_sugars=50,
            min_protein=10,
            max_protein=200,
            min_iron=5,
            max_iron=20,
            min_potassium=1000,
            max_potassium=4000,
            min_carbohydrates=1,
            max_carbohydrates=100,
            min_fat=1,
            max_fat=100,
            min_fiber=1,
            max_fiber=100
        )
        
        # Obtain JWT token pair
        response = self.client.post('/api/login/', {
            'email': self.user_data['email'],
            'password': self.user_data['password']
        }, format='json')
        self.access_token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        # Create recipes
        self.recipes = [
            Recipe.objects.create(
                title=f"Recipe {i}",
                description=f"Description {i}",
                total_calories=200 + i * 50,
                meal_type="main" if i % 2 == 0 else "snack",
                preparation_time=15
            )
            for i in range(1, 5)
        ]
        self.user.save()
    def test_post_weekly_meal_plan(self):
        # Send POST request to generate weekly meal plan
        response = self.client.post("/api/weekly-meal-plan/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Validate weekly plan structure
        weekly_plan = response.data.get("weekly_plan", [])
        self.assertEqual(len(weekly_plan), 7)  # 7 days of the week
        for day_plan in weekly_plan:
            self.assertIn("date", day_plan)
            self.assertIn("recipes", day_plan)
            self.assertIsInstance(day_plan["recipes"], list)

    def test_get_planned_recipes(self):
        # Pre-create a few day plans with recipes
        today = datetime.today().date()
        for i in range(3):
            day_plan = DayPlan.objects.create(user=self.user, date=today + timedelta(days=i))
            DayPlanRecipes.objects.create(day_plan=day_plan, recipe=self.recipes[i])

        # Send GET request
        response = self.client.get("/api/weekly-meal-plan/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Validate planned recipes structure
        planned_recipes = response.data.get("planned_recipes", {})
        self.assertTrue(planned_recipes)

        # Ensure days are present and sorted correctly
        for day, recipes in planned_recipes.items():
            self.assertIsInstance(day, str)
            self.assertIsInstance(recipes, list)

    def test_patch_update_recipe_in_day_plan(self):
        # Create a day plan and assign a recipe
        today = datetime.today().date()
        day_plan = DayPlan.objects.create(user=self.user, date=today)
        current_recipe = self.recipes[0]
        new_recipe = self.recipes[1]
        DayPlanRecipes.objects.create(day_plan=day_plan, recipe=current_recipe)





        # Send PATCH request to update recipe
        patch_data = {
            "day": today.strftime("%Y-%m-%d"),
            "current_recipe_id": current_recipe.id,
            "new_recipe_id": new_recipe.id
        }
        response = self.client.patch("/api/weekly-meal-plan/", patch_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Validate the update
        updated_plan = DayPlanRecipes.objects.filter(day_plan=day_plan, recipe=new_recipe).exists()
        self.assertTrue(updated_plan)

    def test_patch_recipe_not_found(self):
        # Create a day plan with a recipe
        today = datetime.today().date()
        day_plan = DayPlan.objects.create(user=self.user, date=today)
        current_recipe = self.recipes[0]
        DayPlanRecipes.objects.create(day_plan=day_plan, recipe=current_recipe)

        # Send PATCH request with invalid recipe IDs
        patch_data = {
            "day": today.strftime("%Y-%m-%d"),
            "current_recipe_id": 999,  # Non-existent recipe
            "new_recipe_id": 888      # Non-existent recipe
        }
        response = self.client.patch("/api/weekly-meal-plan/", patch_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_duplicate_recipe(self):
        # Create a day plan and assign recipes
        today = datetime.today().date()
        day_plan = DayPlan.objects.create(user=self.user, date=today)
        recipe1 = self.recipes[0]
        recipe2 = self.recipes[1]
        DayPlanRecipes.objects.create(day_plan=day_plan, recipe=recipe1)
        DayPlanRecipes.objects.create(day_plan=day_plan, recipe=recipe2)

        # Try to update recipe1 to recipe2, which already exists in the day plan
        patch_data = {
            "day": today.strftime("%Y-%m-%d"),
            "current_recipe_id": recipe1.id,
            "new_recipe_id": recipe2.id
        }
        response = self.client.patch("/api/weekly-meal-plan/", patch_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)