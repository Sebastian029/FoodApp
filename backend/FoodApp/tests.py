from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from api.models import (Ingredient, DislikedIngredients, RecipeIngredients, UserWeight,
                        Cart, CartIngredient, DayPlanRecipes, DayPlan, UserNutrientPreferences
                        )
from datetime import timedelta, datetime
from django.utils.timezone import now
from django.test import TestCase
from api.models import Recipe, Ingredient, DislikedIngredients, User
from api.utils import select_meals 
from django.contrib.auth import get_user_model
User = get_user_model()



class JWTTestCase(APITestCase):
    def setUp(self):
        self.user_data = {
            'email': 'test@example.com',
            'password': 'password123',
            'name': 'User',
            'surname': 'User'
        }
        self.user = User.objects.create_user(**self.user_data)
        self.url = '/api/login/'  
    def test_jwt_token_obtain_pair(self):
        response = self.client.post('/api/login/', self.user_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

        self.access_token = response.data['access']
        self.refresh_token = response.data['refresh']

    def test_jwt_token_refresh(self):
        response = self.client.post('/api/login/', self.user_data, format='json')
        refresh_token = response.data['refresh']

        refresh_response = self.client.post('/api/token/refresh/', {'refresh': refresh_token}, format='json')
        
        self.assertEqual(refresh_response.status_code, status.HTTP_200_OK)
        
        self.assertIn('access', refresh_response.data)

        self.assertNotEqual(refresh_response.data['access'], response.data['access'])

    def test_protected_view_with_token(self):
        response = self.client.post(self.url, self.user_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        access_token = response.data.get('access')
        self.assertIsNotNone(access_token)  

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        protected_url = '/api/protected/'  
        protected_response = self.client.get(protected_url)

        self.assertEqual(protected_response.status_code, status.HTTP_200_OK)

        self.client.credentials()
   
    def test_access_protected_view_without_token(self):
        protected_url = '/api/protected/'  
        
        response = self.client.get(protected_url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class UserWeightTestCase(APITestCase):
    def setUp(self):
        self.user_data = {
            'email': 'test@example.com',
            'password': 'password123',
            'name': 'User',
            'surname': 'User'
        }
        self.user = User.objects.create_user(**self.user_data)

        self.url = '/api/can-update-weight/'  
        self.client.force_authenticate(user=self.user)

        today = now().date()
        start_of_week = today - timedelta(days=today.weekday())
        self.weekly_weight_entry = UserWeight.objects.create(
            user=self.user,
            weight="70",
            date=start_of_week
        )

    def test_can_update_weight_true(self):
        self.weekly_weight_entry.delete()

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['can_update'])

    def test_can_update_weight_false(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['can_update'])

class EndpointsTestCase(APITestCase):
    def setUp(self):
        self.user_data = {
            'email': 'test@example.com',
            'password': 'password123',
            'name': 'Test',
            'surname': 'User'
        }
        self.user = User.objects.create_user(**self.user_data)
        
        self.ingredient1 = Ingredient.objects.create(name="Tomato")
        self.ingredient2 = Ingredient.objects.create(name="Onion")

        self.client.force_authenticate(user=self.user)

    def test_set_user_nutrient_preferences(self):
        url = '/api/preferences/'  
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

        self.assertEqual(response.status_code, status.HTTP_200_OK)

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
        url = '/api/preferences/'  
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

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertIn('min_calories', response.data)
        self.assertIn('max_calories', response.data)
        self.assertIn('min_sugars', response.data)
        self.assertIn('max_sugars', response.data)

    def test_set_user_nutrient_preferences_with_letters(self):
        url = '/api/preferences/'  
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
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('min_calories', response.data)
        self.assertIn('max_calories', response.data)
        self.assertIn('min_sugars', response.data)
        self.assertIn('max_sugars', response.data)

    def test_set_user_nutrient_preferences_with_missing_fields(self):
        url = '/api/preferences/'  
        data = {
            "min_calories": 1500,
            "max_calories": 2500,
            "min_sugars": 30,
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_user_nutrient_preferences(self):
        self.test_set_user_nutrient_preferences()
        
        url = '/api/preferences/'  
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['min_calories'], 1500)

    def test_post_user_disliked_ingredients(self):
        url = '/api/disliked-ingredients/'  
        data = {"ingredient_ids": [self.ingredient1.id, self.ingredient2.id]}
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["message"], "Disliked ingredients saved successfully.")
        
        self.assertTrue(DislikedIngredients.objects.filter(user=self.user, ingredient=self.ingredient1).exists())
        self.assertTrue(DislikedIngredients.objects.filter(user=self.user, ingredient=self.ingredient2).exists())

    def test_post_user_disliked_ingredients_with_invalid_id(self):
        url = '/api/disliked-ingredients/'  

        invalid_ingredient_id = 99999999  
        data = {"ingredient_ids": [invalid_ingredient_id]}
        
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertIn('ingredient_ids', response.data)  
        self.assertIn(f"Invalid ingredient id(s): {invalid_ingredient_id}", str(response.data))





class SelectMealsTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(email='test@example.com', password='testpass')
      
        self.user_nutrient_preferences = UserNutrientPreferences.objects.create(
            user=self.user,
            min_calories=1000,
            max_calories=3000,
            min_sugars=10,
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

        ingredients = [
            "Tomato", "Chicken", "Lettuce", "Beef", "Pasta", "Quinoa", "Avocado",
            "Onion", "Garlic", "Mushroom", "Cheese", "Egg", "Broccoli", "Carrot",
            "Rice", "Peppers", "Potatoes", "Spinach", "Basil", "Milk", "Yogurt"
        ]
        self.ingredients = {name: Ingredient.objects.create(name=name) for name in ingredients}

        DislikedIngredients.objects.create(user=self.user, ingredient=self.ingredients["Tomato"])
        DislikedIngredients.objects.create(user=self.user, ingredient=self.ingredients["Chicken"])

        recipes_data = [
            ("Chicken Caesar Salad", ["Chicken", "Lettuce", "Cheese", "Garlic"]),
            ("Spaghetti Bolognese", ["Beef", "Pasta", "Tomato", "Onion"]),
            ("Vegan Buddha Bowl", ["Quinoa", "Avocado", "Carrot", "Spinach"]),
            ("Greek Yogurt Parfait", ["Yogurt", "Berries", "Granola"]),
            ("Beef Tacos", ["Beef", "Onion", "Peppers", "Cheese"]),
            ("Eggplant Parmesan", ["Egg", "Tomato", "Cheese", "Basil"]),
            ("Pancakes", ["Milk", "Egg", "Flour", "Sugar"]),
            ("Chicken Stir Fry", ["Chicken", "Rice", "Peppers", "Onion"]),
            ("Vegetable Soup", ["Carrot", "Potatoes", "Onion", "Garlic"]),
            ("Grilled Cheese Sandwich", ["Cheese", "Bread", "Butter", "Tomato"]),
            ("Avocado Toast", ["Avocado", "Bread", "Egg", "Salt"]),
            ("Shrimp Alfredo Pasta", ["Shrimp", "Pasta", "Cream", "Cheese"]),
            ("Berry Smoothie", ["Yogurt", "Berries", "Milk", "Honey"]),
            ("Quinoa Salad", ["Quinoa", "Tomato", "Cucumber", "Spinach"]),
            ("Beef Burger", ["Beef", "Bun", "Lettuce", "Cheese"]),
            ("Oatmeal with Fruit", ["Oats", "Milk", "Banana", "Berries"]),
            ("Stuffed Bell Peppers", ["Peppers", "Rice", "Beef", "Cheese"]),
            ("Minestrone Soup", ["Pasta", "Carrot", "Tomato", "Onion"]),
            ("Chicken Curry", ["Chicken", "Rice", "Coconut Milk", "Garlic"]),
            ("Vegetable Stir Fry", ["Broccoli", "Carrot", "Mushroom", "Onion"]),
            ("Fish Tacos", ["Fish", "Tortilla", "Lettuce", "Avocado"]),
            ("Cheese Pizza", ["Cheese", "Tomato", "Basil", "Flour"]),
            ("French Toast", ["Bread", "Egg", "Milk", "Sugar"]),
            ("Grilled Salmon", ["Salmon", "Lemon", "Garlic", "Potatoes"]),
            ("Tofu Scramble", ["Tofu", "Spinach", "Onion", "Mushroom"])
        ]

        meal_types = ["dinner", "snack", "breakfast",  "lunch"]
        for index, (title, ingredient_names) in enumerate(recipes_data):
            meal_type = meal_types[index % len(meal_types)]
            recipe = Recipe.objects.create(
                title=title,
                description="Des",
                total_calories=300 + len(ingredient_names) * 50,
                sugars=5 + len(ingredient_names),
                protein=10 + len(ingredient_names) * 2,
                fat=5 + len(ingredient_names),
                carbohydrates=10 + len(ingredient_names) * 2,
                fiber=2 + len(ingredient_names) * 0.5,
                iron=3 + len(ingredient_names) * 0.5,
                potassium=400 + len(ingredient_names) * 100,
                preparation_time=15 + len(ingredient_names) * 2,
                preparation_guide="Prepare",
                meal_type=meal_type
            )
            
            for ingredient_name in ingredient_names:
                ingredient = self.ingredients.get(ingredient_name)
                if ingredient:
                    RecipeIngredients.objects.create(
                        recipe=recipe,
                        ingredient=ingredient,
                        quantity=1.0, 
                        unit="g"  
                    )

    def test_basic_selection(self):
        selected_meals = select_meals(optimize_field='protein', objective='maximize', user=self.user)

        self.assertTrue(len(selected_meals) > 0, "Expected meals to be selected")

    def test_nutritional_preferences_constraints(self):
        selected_meals = select_meals(optimize_field='protein', objective='maximize', user=self.user)
        user_preferences = UserNutrientPreferences.objects.get(user=self.user)
        
        total_calories = sum(int(float(meal.total_calories)) for meal in selected_meals)  
        total_sugars = sum(int(float(meal.sugars)) for meal in selected_meals)            
        total_protein = sum(int(float(meal.protein)) for meal in selected_meals)          
        total_iron = sum(int(float(meal.iron)) for meal in selected_meals)                
        total_potassium = sum(int(float(meal.potassium)) for meal in selected_meals)
        total_carbohydrates = sum(int(float(meal.carbohydrates)) for meal in selected_meals)  
        total_fat = sum(int(float(meal.fat)) for meal in selected_meals)                     
        total_fiber = sum(int(float(meal.fiber)) for meal in selected_meals)   

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
        selected_meals = select_meals(optimize_field='protein', objective='maximize', user=self.user)
        meal_types = [meal.meal_type for meal in selected_meals]
        expected_meal_types = ["lunch", "dinner", "breakfast"]

        for meal_type in expected_meal_types[:]:  
            if meal_type in meal_types:
                expected_meal_types.remove(meal_type)
                
        self.assertEqual(expected_meal_types, [], f"Missing meal types: {expected_meal_types}")
                
    def test_no_disliked_ingredients(self):
        selected_meals = select_meals(optimize_field='protein', objective='maximize', user=self.user)
        disliked_ingredients = DislikedIngredients.objects.filter(user=self.user).values_list('ingredient__name', flat=True)

        for meal in selected_meals:
            meal_ingredients = meal.ingredients.values_list('name', flat=True)  
            for disliked_ingredient in disliked_ingredients:
                self.assertNotIn(
                    disliked_ingredient, meal_ingredients,
                    f"Disliked {disliked_ingredient}' in '{meal.title}'."
                )

                
class CartTestCase(APITestCase):
    def setUp(self):
        self.user_data = {
            'email': 'test@example.com',
            'password': 'password123'
        }
        self.user = User.objects.create_user(**self.user_data)

        response = self.client.post('/api/login/', self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)  
        self.access_token = response.data['access']

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

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

        self.recipe_ingredient_1 = Ingredient.objects.create(name="Eggs")
        self.recipe_ingredient_2 = Ingredient.objects.create(name="Milk")

        RecipeIngredients.objects.create(recipe=self.recipe, ingredient=self.recipe_ingredient_1, quantity=3, unit="units")
        RecipeIngredients.objects.create(recipe=self.recipe, ingredient=self.recipe_ingredient_2, quantity=2, unit="cups")


    def test_update_quantity(self):
        response = self.client.patch(
            f'/api/cart/{self.cart_ingredient.id}/', 
            {'quantity': 5},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.cart_ingredient.refresh_from_db()  
        self.assertEqual(self.cart_ingredient.quantity, 5) 

    def test_remove_ingredient(self):
        response = self.client.delete(f'/api/cart/{self.cart_ingredient.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        with self.assertRaises(CartIngredient.DoesNotExist):
            self.cart_ingredient.refresh_from_db()  

    def test_clear_cart(self):
        additional_ingredient = Ingredient.objects.create(name="Sugar")
        CartIngredient.objects.create(
            cart=self.cart,
            ingredient=additional_ingredient,
            quantity=1,
            unit="cups"
        )

        response = self.client.delete('/api/cart/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(CartIngredient.objects.filter(cart=self.cart).count(), 0)

    def test_add_ingredient_to_cart(self):
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

        ingredient = Ingredient.objects.get(name="Sugar")
        cart_ingredient = CartIngredient.objects.get(cart=self.cart, ingredient=ingredient)
        self.assertEqual(cart_ingredient.quantity, 3)
        self.assertEqual(cart_ingredient.unit, 'cups')

    def test_add_multiple_ingredients_to_cart(self):
        ingredient_data = {
            'ingredients': [
                {'ingredient_name': 'Sugar', 'quantity': 3, 'unit': 'cups'},
                {'ingredient_name': 'Butter', 'quantity': 2, 'unit': 'tbsp'}
            ]
        }

        response = self.client.post('/api/cart/', ingredient_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        sugar = Ingredient.objects.get(name="Sugar")
        butter = Ingredient.objects.get(name="Butter")

        cart_ingredient_sugar = CartIngredient.objects.get(cart=self.cart, ingredient=sugar)
        cart_ingredient_butter = CartIngredient.objects.get(cart=self.cart, ingredient=butter)

        self.assertEqual(cart_ingredient_sugar.quantity, 3)
        self.assertEqual(cart_ingredient_butter.quantity, 2)
        self.assertEqual(cart_ingredient_sugar.unit, 'cups')
        self.assertEqual(cart_ingredient_butter.unit, 'tbsp')

    def test_add_ingredients_by_recipe(self):
        recipe_data = {
            'recipe_id': self.recipe.id
        }

        response = self.client.post('/api/cart/', recipe_data, format='json')


        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        cart_ingredient_eggs = CartIngredient.objects.get(cart=self.cart, ingredient=self.recipe_ingredient_1)
        cart_ingredient_milk = CartIngredient.objects.get(cart=self.cart, ingredient=self.recipe_ingredient_2)

        self.assertEqual(cart_ingredient_eggs.quantity, 3)
        self.assertEqual(cart_ingredient_milk.quantity, 2)
        self.assertEqual(cart_ingredient_eggs.unit, 'units')  
        self.assertEqual(cart_ingredient_milk.unit, 'cups')  

    def test_add_invalid_ingredient_quantity(self):
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

        ingredient_data_invalid = {
            'ingredients': [
                {
                    'ingredient_name': 'Sugar',
                    'quantity': 'abc',  
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
        self.user_data = {
            'email': 'test@example.com',
            'password': 'password123',
            'name': 'User',
            'surname': 'User'
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
        
        response = self.client.post('/api/login/', {
            'email': self.user_data['email'],
            'password': self.user_data['password']
        }, format='json')
        self.access_token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        self.recipes = [
            Recipe.objects.create(
                title=f"Recipe {i}",
                description="Des",
                total_calories=200 + i * 50,
                meal_type="lunch",
                preparation_time=15
            )
            for i in range(1, 5)
        ]
        self.user.save()
        
    def test_post_weekly_meal_plan(self):
        response = self.client.post("/api/weekly-meal-plan/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        weekly_plan = response.data.get("weekly_plan", [])
        self.assertEqual(len(weekly_plan), 7) 
        for day_plan in weekly_plan:
            self.assertIn("date", day_plan)
            self.assertIn("recipes", day_plan)
            self.assertIsInstance(day_plan["recipes"], list)

    def test_get_planned_recipes(self):
        today = datetime.today().date()
        for i in range(3):
            day_plan = DayPlan.objects.create(user=self.user, date=today + timedelta(days=i))
            DayPlanRecipes.objects.create(day_plan=day_plan, recipe=self.recipes[i])

        response = self.client.get("/api/weekly-meal-plan/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        planned_recipes = response.data.get("planned_recipes", {})
        self.assertTrue(planned_recipes)

        for day, recipes in planned_recipes.items():
            self.assertIsInstance(day, str)
            self.assertIsInstance(recipes, list)

    def test_patch_update_recipe_in_day_plan(self):
        today = datetime.today().date()
        day_plan = DayPlan.objects.create(user=self.user, date=today)
        current_recipe = self.recipes[0]
        new_recipe = self.recipes[1]
        DayPlanRecipes.objects.create(day_plan=day_plan, recipe=current_recipe)

        patch_data = {
            "day": today.strftime("%Y-%m-%d"),
            "current_recipe_id": current_recipe.id,
            "new_recipe_id": new_recipe.id
        }
        response = self.client.patch("/api/weekly-meal-plan/", patch_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        updated_plan = DayPlanRecipes.objects.filter(day_plan=day_plan, recipe=new_recipe).exists()
        self.assertTrue(updated_plan)

    def test_patch_recipe_not_found(self):
        today = datetime.today().date()
        day_plan = DayPlan.objects.create(user=self.user, date=today)
        current_recipe = self.recipes[0]
        DayPlanRecipes.objects.create(day_plan=day_plan, recipe=current_recipe)

        patch_data = {
            "day": today.strftime("%Y-%m-%d"),
            "current_recipe_id": 999,  
            "new_recipe_id": 888      
        }
        response = self.client.patch("/api/weekly-meal-plan/", patch_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_duplicate_recipe(self):
        today = datetime.today().date()
        day_plan = DayPlan.objects.create(user=self.user, date=today)
        recipe1 = self.recipes[0]
        recipe2 = self.recipes[1]
        DayPlanRecipes.objects.create(day_plan=day_plan, recipe=recipe1)
        DayPlanRecipes.objects.create(day_plan=day_plan, recipe=recipe2)

        patch_data = {
            "day": today.strftime("%Y-%m-%d"),
            "current_recipe_id": recipe1.id,
            "new_recipe_id": recipe2.id
        }
        response = self.client.patch("/api/weekly-meal-plan/", patch_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)