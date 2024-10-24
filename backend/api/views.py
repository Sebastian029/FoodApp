# api/views.py
from rest_framework import generics
from .models import User, Recipe, Ingredient, RecipeIngredients, DayPlan, DayPlanRecipes, RatedRecipes, UserWeight, DislikedIngredients, UserIngredients
from .serializers import (
    UserSerializer, RecipeSerializer, IngredientSerializer, 
    RecipeIngredientsSerializer, DayPlanSerializer, DayPlanRecipesSerializer, 
    RatedRecipesSerializer, UserWeightSerializer, DislikedIngredientsSerializer, 
    UserIngredientsSerializer
)

# from .utils import 

# User Views
class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Recipe Views
class RecipeListCreateView(generics.ListCreateAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

class RecipeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer


# Ingredient Views
class IngredientListCreateView(generics.ListCreateAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer

class IngredientDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer

# RecipeIngredients Views
class RecipeIngredientsListCreateView(generics.ListCreateAPIView):
    queryset = RecipeIngredients.objects.all()
    serializer_class = RecipeIngredientsSerializer

class RecipeIngredientsDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = RecipeIngredients.objects.all()
    serializer_class = RecipeIngredientsSerializer

# DayPlan Views
class DayPlanListCreateView(generics.ListCreateAPIView):
    queryset = DayPlan.objects.all()
    serializer_class = DayPlanSerializer

class DayPlanDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DayPlan.objects.all()
    serializer_class = DayPlanSerializer

# DayPlanRecipes Views
class DayPlanRecipesListCreateView(generics.ListCreateAPIView):
    queryset = DayPlanRecipes.objects.all()
    serializer_class = DayPlanRecipesSerializer

class DayPlanRecipesDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DayPlanRecipes.objects.all()
    serializer_class = DayPlanRecipesSerializer

# RatedRecipes Views
class RatedRecipesListCreateView(generics.ListCreateAPIView):
    queryset = RatedRecipes.objects.all()
    serializer_class = RatedRecipesSerializer

class RatedRecipesDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = RatedRecipes.objects.all()
    serializer_class = RatedRecipesSerializer

# UserWeight Views
class UserWeightListCreateView(generics.ListCreateAPIView):
    queryset = UserWeight.objects.all()
    serializer_class = UserWeightSerializer

class UserWeightDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserWeight.objects.all()
    serializer_class = UserWeightSerializer

# DislikedIngredients Views
class DislikedIngredientsListCreateView(generics.ListCreateAPIView):
    queryset = DislikedIngredients.objects.all()
    serializer_class = DislikedIngredientsSerializer

class DislikedIngredientsDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DislikedIngredients.objects.all()
    serializer_class = DislikedIngredientsSerializer

# UserIngredients Views
class UserIngredientsListCreateView(generics.ListCreateAPIView):
    queryset = UserIngredients.objects.all()
    serializer_class = UserIngredientsSerializer

class UserIngredientsDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserIngredients.objects.all()
    serializer_class = UserIngredientsSerializer


# api/views.py
import csv
from datetime import datetime
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Recipe
from .serializers import RecipeSerializer

import csv
from datetime import datetime
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from api.models import Recipe,Ingredient, RecipeIngredients  # Adjust import based on your actual model structure

@api_view(['GET'])
def upload_recipes_csv(request):
    # Path to your CSV file
    file_path = 'data.csv'  # Directly reference the CSV in the root directory

    # Read the CSV file
    try:
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            # Specify the delimiter as ';'
            reader = csv.DictReader(csvfile, delimiter=';')

            for row in reader:
              

                # Create and save the Recipe instance
                recipe_data = {
                    'title': row['name'],
                    'description': row['short_description'],
                    'total_calories': row['total_calories'],
                    'sugars': row['sugars'],
                    'protein': row['protein'],
                    'iron': row['iron'],
                    'potassium': row['potassium'],
                    'potassium': row['potassium'],
                    'preparation_time': row['preparation_time'],
                    'preparation_guide': row['preparation_guide'],
                    'meal_type': row['meal_type'],
                    
                    
                }

                # Create the recipe object
                recipe = Recipe.objects.create(**recipe_data)

                # Handle ingredients if they exist
                if 'ingredients' in row:
                    ingredients = [ingredient.strip() for ingredient in row['ingredients'].split(',')]  # Assuming this column contains comma-separated ingredients
                    for ingredient_name in ingredients:
                        # Check if ingredient exists or create it
                        ingredient_obj, created = Ingredient.objects.get_or_create(name=ingredient_name)

                        # Create a relationship in the recipe_ingredients table
                        RecipeIngredients.objects.get_or_create(recipe_id=recipe.id, ingredient_id=ingredient_obj.id)

        return Response({'message': 'Recipes uploaded successfully!'}, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
