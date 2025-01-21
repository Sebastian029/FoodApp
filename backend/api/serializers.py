from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.utils.timezone import now

from .models import (
    User, Recipe, Ingredient, RecipeIngredients, 
    DayPlanRecipes,  UserWeight, 
    UserNutrientPreferences,Cart,
    CartIngredient, CartIngredient
)

User = get_user_model()

# user auth
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'name', 'surname', 'password', 'confirm_password')

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError("Passwords must match")
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password')

        user = User(**validated_data)
        user.set_password(validated_data['password'])  
        user.save()
        UserNutrientPreferences.objects.create(user=user)
        return user


# recipes and planner_screen

        
class AllIngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name'] 
        
class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '_all__'

class RecipeIngredientsSerializer(serializers.ModelSerializer):
    ingredient = IngredientSerializer()  
    class Meta:
        model = RecipeIngredients
        fields = ['ingredient', 'quantity', 'unit']
        
class RecipeSerializer(serializers.ModelSerializer):
    ingredients = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ['id', 'title', 'description', 'total_calories', 'sugars', 'protein', 'fat', 'carbohydrates', 'fiber',
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
    
class DayPlanRecipesSerializer(serializers.ModelSerializer):
    class Meta:
        model = DayPlanRecipes
        fields = '__all__'

class NutrientSummarySerializer(serializers.Serializer):
    total_calories = serializers.FloatField()
    total_sugars = serializers.FloatField()
    total_protein = serializers.FloatField()
    total_iron = serializers.FloatField()
    total_potassium = serializers.FloatField()

# cart
class CartIngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartIngredient
        fields = ['id', 'ingredient', 'quantity', 'unit', 'bought']  

class CartSerializer(serializers.ModelSerializer):
    ingredients = CartIngredientSerializer(many=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'ingredients']


# user screen
class UserWeightSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserWeight
        fields = ['weight', 'date']

    def validate_date(self, value):
        if value > timezone.now().date():
            raise serializers.ValidationError("The date cannot be in the future.")
        return value

class DietTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserNutrientPreferences
        fields = ['diet_type']

    def validate_diet_type(self, value):
        if value not in dict(UserNutrientPreferences.DIET_CHOICES):
            raise serializers.ValidationError("Invalid diet type.")
        return value


class UserWeightSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserWeight
        fields = ['id',  'weight', 'date']

class UserNutrientPreferencesSerializer(serializers.ModelSerializer):
    min_calories = serializers.IntegerField(min_value=0)
    max_calories = serializers.IntegerField(min_value=0)
    min_sugars = serializers.IntegerField(min_value=0)
    max_sugars = serializers.IntegerField(min_value=0)
    min_protein = serializers.IntegerField(min_value=0)
    max_protein = serializers.IntegerField(min_value=0)
    min_fat = serializers.IntegerField(min_value=0)
    max_fat = serializers.IntegerField(min_value=0)
    min_carbohydrates = serializers.IntegerField(min_value=0)
    max_carbohydrates = serializers.IntegerField(min_value=0)
    min_fiber = serializers.IntegerField(min_value=0)
    max_fiber = serializers.IntegerField(min_value=0)
    min_iron = serializers.IntegerField(min_value=0)
    max_iron = serializers.IntegerField(min_value=0)
    min_potassium = serializers.IntegerField(min_value=0)
    max_potassium = serializers.IntegerField(min_value=0)

    class Meta:
        model = UserNutrientPreferences
        fields = [
            'min_calories', 'max_calories',
            'min_sugars', 'max_sugars',
            'min_protein', 'max_protein',
            'min_iron', 'max_iron',
            'min_potassium', 'max_potassium',
            'min_fat', 'max_fat',
            'min_carbohydrates', 'max_carbohydrates',
            'min_fiber', 'max_fiber'
        ]
    
    def validate(self, data):
        nutrient_pairs = [
            ('min_calories', 'max_calories'),
            ('min_sugars', 'max_sugars'),
            ('min_protein', 'max_protein'),
            ('min_iron', 'max_iron'),
            ('min_potassium', 'max_potassium'),
            ('min_fat', 'max_fat'),
            ('min_carbohydrates', 'max_carbohydrates'),
            ('min_fiber', 'max_fiber')
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
        invalid_ids = [id for id in value if not Ingredient.objects.filter(id=id).exists()]
        if invalid_ids:
            raise ValidationError(f"Invalid ingredient id(s): {', '.join(map(str, invalid_ids))}")
        return value










        


    
