from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import (
    User, Recipe, Ingredient, RecipeIngredients, 
    DayPlan, DayPlanRecipes, RatedRecipes, UserWeight, 
    DislikedIngredients, UserIngredients, UserNutrientPreferences,
    Cart, CartIngredient, CartIngredient
    
)
from django.contrib.auth import get_user_model
from django.utils.timezone import now

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
        
class UserNutrientPreferencesSerializer(serializers.ModelSerializer):
    min_calories = serializers.IntegerField(min_value=1)
    max_calories = serializers.IntegerField(min_value=1)
    min_sugars = serializers.IntegerField(min_value=1)
    max_sugars = serializers.IntegerField(min_value=1)
    min_protein = serializers.IntegerField(min_value=1)
    max_protein = serializers.IntegerField(min_value=1)
    min_iron = serializers.IntegerField(min_value=1)
    max_iron = serializers.IntegerField(min_value=1)
    min_potassium = serializers.IntegerField(min_value=1)
    max_potassium = serializers.IntegerField(min_value=1)

    class Meta:
        model = UserNutrientPreferences
        fields = [
            'min_calories', 'max_calories',
            'min_sugars', 'max_sugars',
            'min_protein', 'max_protein',
            'min_iron', 'max_iron',
            'min_potassium', 'max_potassium'
        ]
    
    def validate(self, data):
        nutrient_pairs = [
            ('min_calories', 'max_calories'),
            ('min_sugars', 'max_sugars'),
            ('min_protein', 'max_protein'),
            ('min_iron', 'max_iron'),
            ('min_potassium', 'max_potassium'),
        ]
        
        for min_field, max_field in nutrient_pairs:
            min_value = data.get(min_field)
            max_value = data.get(max_field)
            if min_value and max_value and min_value > max_value:
                raise serializers.ValidationError(
                    {min_field: f"{min_field.replace('_', ' ').capitalize()} should be less than or equal to {max_field.replace('_', ' ')}"}
                )
        
        return data

class DislikedIngredientsSerializer(serializers.Serializer):
    ingredient_ids = serializers.ListField(
        child=serializers.IntegerField(), required=True
    )

    def validate_ingredient_ids(self, value):
        # Check if all ingredient IDs are valid
        invalid_ids = [id for id in value if not Ingredient.objects.filter(id=id).exists()]
        if invalid_ids:
            raise ValidationError(f"Invalid ingredient id(s): {', '.join(map(str, invalid_ids))}")
        return value
    
    
    
class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '_all__'

class RecipeIngredientsSerializer(serializers.ModelSerializer):
    ingredient = IngredientSerializer()  # Serialize the Ingredient model

    class Meta:
        model = RecipeIngredients
        fields = ['ingredient', 'quantity', 'unit']
        
class RecipeSerializer(serializers.ModelSerializer):
    ingredients = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ['id', 'title', 'description', 'total_calories', 'sugars', 'protein', 
                  'iron', 'potassium', 'preparation_time', 'preparation_guide', 
                  'meal_type', 'ingredients']

    def get_ingredients(self, obj):
        recipe_ingredients = obj.recipeingredients_set.all()
        ingredient_data = []
        
        for ri in recipe_ingredients:
            ingredient_data.append({
                'ingredient_name': ri.ingredient.name,
                'quantity': ri.quantity,
                'unit': ri.unit
            })
        
        return ingredient_data

class CartIngredientSerializer(serializers.ModelSerializer):
    ingredient = IngredientSerializer()

    class Meta:
        model = CartIngredient
        fields = ['ingredient', 'quantity', 'unit']

class CartSerializer(serializers.ModelSerializer):
    ingredients = CartIngredientSerializer(many=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'ingredients']

class UserWeightSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserWeight
        fields = ['weight', 'date']

    def validate_date(self, value):
        # Ensure the date is not in the future
        if value > timezone.now().date():
            raise serializers.ValidationError("The date cannot be in the future.")
        return value


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


class UserIngredientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserIngredients
        fields = '__all__'

