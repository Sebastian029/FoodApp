from rest_framework import serializers
from .models import (
    User, Recipe, Ingredient, RecipeIngredients, 
    DayPlan, DayPlanRecipes, RatedRecipes, UserWeight, 
    DislikedIngredients, UserIngredients
)
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'name', 'surname', 'password', 'confirm_password')

    def validate(self, attrs):
        # Check that the password and confirm_password match
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError("Passwords must match")
        return attrs

    def create(self, validated_data):
        # Remove confirm_password as it is not a field in the User model
        validated_data.pop('confirm_password')

        # Create the user and set the password
        user = User(**validated_data)
        user.set_password(validated_data['password'])  # Hash the password
        user.save()
        return user

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

