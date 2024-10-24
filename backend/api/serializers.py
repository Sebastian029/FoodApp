from rest_framework import serializers
from .models import (
    User, Recipe, Ingredient, RecipeIngredients, 
    DayPlan, DayPlanRecipes, RatedRecipes, UserWeight, 
    DislikedIngredients, UserIngredients
)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = '__all__'

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'

class RecipeIngredientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeIngredients
        fields = '__all__'

class DayPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = DayPlan
        fields = '__all__'

class DayPlanRecipesSerializer(serializers.ModelSerializer):
    class Meta:
        model = DayPlanRecipes
        fields = '__all__'

class RatedRecipesSerializer(serializers.ModelSerializer):
    class Meta:
        model = RatedRecipes
        fields = '__all__'

class UserWeightSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserWeight
        fields = '__all__'

class DislikedIngredientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DislikedIngredients
        fields = '__all__'

class UserIngredientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserIngredients
        fields = '__all__'


