# api/views.py
from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from datetime import timedelta, datetime
from django.utils.timezone import now

from .serializers import RegisterSerializer
from .models import (User, Recipe, Ingredient, RecipeIngredients,
                     DayPlan, DayPlanRecipes, RatedRecipes, UserWeight,
                     DislikedIngredients, UserIngredients, UserNutrientPreferences,
                     Cart, Ingredient, CartIngredient
)
from .serializers import (
    UserSerializer, RecipeSerializer, IngredientSerializer, 
    RecipeIngredientsSerializer, DayPlanSerializer, DayPlanRecipesSerializer, 
    RatedRecipesSerializer, UserWeightSerializer, DislikedIngredientsSerializer, 
    UserIngredientsSerializer, UserNutrientPreferencesSerializer,
    CartSerializer, IngredientSerializer
)
from .utils import  upload_recipes_from_csv, plan_meals_for_week


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny]


class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        return Response({"message": "You have access to this view."})

class UserListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    
class UserNutrientPreferencesView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            preferences = UserNutrientPreferences.objects.get(user=request.user)
            serializer = UserNutrientPreferencesSerializer(preferences, data=request.data, partial=True)
        except UserNutrientPreferences.DoesNotExist:
            serializer = UserNutrientPreferencesSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
    
    def get(self, request):
        try:
            preferences = UserNutrientPreferences.objects.get(user=request.user)
            serializer = UserNutrientPreferencesSerializer(preferences)
            return Response(serializer.data)
        except UserNutrientPreferences.DoesNotExist:
            return Response({"detail": "Preferences not set."}, status=status.HTTP_404_NOT_FOUND)

# Ingredient Views
class IngredientListCreateView(generics.ListCreateAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    
    
    
class UserDislikedIngredientsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        disliked_ingredients = DislikedIngredients.objects.filter(user=user)
        ingredients = [item.ingredient for item in disliked_ingredients]
        serializer = IngredientSerializer(ingredients, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = DislikedIngredientsSerializer(data=request.data)
        if serializer.is_valid():
            ingredient_ids = serializer.validated_data['ingredient_ids']
            user = request.user

            # Clear any existing disliked ingredients for this user
            DislikedIngredients.objects.filter(user=user).delete()

            # Add new disliked ingredients
            disliked_ingredients = [
                DislikedIngredients(user=user, ingredient=Ingredient.objects.get(id=ingredient_id))
                for ingredient_id in ingredient_ids
            ]
            DislikedIngredients.objects.bulk_create(disliked_ingredients)

            return Response({"message": "Disliked ingredients saved successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Recipe Views
class RecipeListCreateView(generics.ListCreateAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

class RecipeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer


class RecipeListView(APIView):
    def get(self, request):
        recipes = Recipe.objects.all()
        serializer = RecipeSerializer(recipes, many=True)
        return Response(serializer.data)
    
class RecipeTypeView(APIView):
    def get(self, request):
        # Get the 'meal_type' parameter from the query parameters (if provided)
        meal_type = request.query_params.get('meal_type', None)
        
        # If 'meal_type' is provided, filter the recipes by that type
        if meal_type:
            recipes = Recipe.objects.filter(meal_type=meal_type)
        else:
            # If no 'meal_type' is provided, return all recipes
            recipes = Recipe.objects.all()
        
        # Serialize the filtered (or all) recipes
        serializer = RecipeSerializer(recipes, many=True)
        
        # Return the response
        return Response(serializer.data)
    
    
class UpdateWeightView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure this line is present
    def post(self, request):
        user = request.user
        weight = request.data.get('weight')
        date = request.data.get('date', now().date())

        # Ensure the user is authenticated
        if not user.is_authenticated:
            return Response({"error": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)

        # Calculate the start and end of the current week (Monday to Sunday)
        today = now().date()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)

        # Check if there is already an entry for the current week
        weekly_entry_exists = UserWeight.objects.filter(
            user=user,
            date__range=[start_of_week, end_of_week]
        ).exists()

        if weekly_entry_exists:
            return Response({"error": "You can only update weight once per week."}, status=status.HTTP_400_BAD_REQUEST)

        # Create a new weight entry
        serializer = UserWeightSerializer(data={'user': user.id, 'weight': weight, 'date': date})
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CanUpdateWeightView(APIView):
    permission_classes = [IsAuthenticated]  
    def get(self, request):
        user = request.user

        # Ensure the user is authenticated
        if not user.is_authenticated:
            return Response({"error": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)

        # Calculate the start and end of the current week (Monday to Sunday)
        today = now().date()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)

        # Check if there is already an entry for the current week
        weekly_entry_exists = UserWeight.objects.filter(
            user=user,
            date__range=[start_of_week, end_of_week]
        ).exists()

        # Return true if the user can update weight, false otherwise
        can_update = not weekly_entry_exists
        return Response({"can_update": can_update}, status=status.HTTP_200_OK)
    
class CartAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    @staticmethod
    def is_positive_number(value):
        """Check if the value is a positive number (either int or float)."""
        return isinstance(value, (int, float)) and value > 0
    
    def get_cart(self, user):
        """
        Get or create the user's cart.
        """
        cart, created = Cart.objects.get_or_create(user=user)
        return cart

    def post(self, request):
        """
        Adds ingredients to the user's cart. Supports adding ingredients
        either by providing a list of ingredients or by providing a recipe ID.
        """
        user = request.user
        cart = self.get_cart(user)  # This line ensures that the cart is created or fetched

        ingredients_data = request.data.get('ingredients')
        recipe_id = request.data.get('recipe_id')

        # If ingredients are provided
        if ingredients_data:
            for item in ingredients_data:
                quantity = item.get("quantity")
                if not self.is_positive_number(quantity):
                    return Response({"message": "Quantity must be a positive number."}, status=status.HTTP_400_BAD_REQUEST)
                ingredient, created = Ingredient.objects.get_or_create(
                    name=item['ingredient_name']
                )

                # Check if the ingredient already exists in the cart
                existing_cart_ingredient = CartIngredient.objects.filter(cart=cart, ingredient=ingredient).first()

                if existing_cart_ingredient:
                    if existing_cart_ingredient.unit != item['unit']:
                        CartIngredient.objects.create(
                            cart=cart,
                            ingredient=ingredient,
                            quantity=item['quantity'],
                            unit=item['unit']
                        )
                    else:
                        existing_cart_ingredient.quantity += item['quantity']
                        existing_cart_ingredient.save()
                else:
                    CartIngredient.objects.create(
                        cart=cart,
                        ingredient=ingredient,
                        quantity=item['quantity'],
                        unit=item['unit']
                    )

            return Response({"message": "Ingredients added to cart."}, status=status.HTTP_201_CREATED)

        # If a recipe ID is provided
        elif recipe_id:
            try:
                recipe = Recipe.objects.get(id=recipe_id)
                serializer = RecipeSerializer(recipe)
                ingredients = serializer.data.get('ingredients')

                if not ingredients:
                    return Response({"message": "No ingredients found in this recipe."}, status=status.HTTP_404_NOT_FOUND)

                for item in ingredients:
                    quantity = item.get("quantity")
                    if not self.is_positive_number(quantity):
                        return Response({"message": "Quantity must be a positive number."}, status=status.HTTP_400_BAD_REQUEST)
                    ingredient, created = Ingredient.objects.get_or_create(
                        name=item['ingredient_name']
                    )

                    existing_cart_ingredient = CartIngredient.objects.filter(cart=cart, ingredient=ingredient).first()

                    if existing_cart_ingredient:
                        if existing_cart_ingredient.unit != item['unit']:
                            CartIngredient.objects.create(
                                cart=cart,
                                ingredient=ingredient,
                                quantity=item['quantity'],
                                unit=item['unit']
                            )
                        else:
                            existing_cart_ingredient.quantity += item['quantity']
                            existing_cart_ingredient.save()
                    else:
                        CartIngredient.objects.create(
                            cart=cart,
                            ingredient=ingredient,
                            quantity=item['quantity'],
                            unit=item['unit']
                        )

                return Response({"message": "Ingredients from recipe added to cart."}, status=status.HTTP_201_CREATED)

            except Recipe.DoesNotExist:
                return Response({"message": "Recipe not found."}, status=status.HTTP_404_NOT_FOUND)

        return Response({"message": "No ingredients or recipe ID provided."}, status=status.HTTP_400_BAD_REQUEST)
    def get(self, request):
        """
        Retrieves the ingredients in the user's cart.
        """
        user = request.user
        cart = self.get_cart(user)

        cart_ingredients = CartIngredient.objects.filter(cart=cart)
        cart_ingredients_data = []

        for item in cart_ingredients:
            cart_ingredients_data.append({
                'id': item.id,
                'ingredient_name': item.ingredient.name,
                'quantity': item.quantity,
                'unit': item.unit,
                'bought': item.bought  # Include bought status
            })

        return Response({'cart_ingredients': cart_ingredients_data}, status=status.HTTP_200_OK)

    def patch(self, request, ingredient_id):
        """
        Update the quantity or 'bought' status of a specific ingredient in the cart.
        """
        user = request.user
        cart = self.get_cart(user)

        try:
            cart_ingredient = CartIngredient.objects.get(cart=cart, id=ingredient_id)
        except CartIngredient.DoesNotExist:
            return Response({"message": "Ingredient not found in cart."}, status=status.HTTP_404_NOT_FOUND)

        # Update quantity if provided
        quantity = request.data.get('quantity')
        if quantity is not None:
            cart_ingredient.quantity = quantity

        # Update bought status if provided
        bought = request.data.get('bought')
        if bought is not None:
            cart_ingredient.bought = bought

        cart_ingredient.save()
        return Response({"message": "Cart ingredient updated."}, status=status.HTTP_200_OK)

    def delete(self, request, ingredient_id=None):
        """
        Remove a specific ingredient from the cart, or clear the entire cart if no id is provided.
        The removal will only affect the cart, not the original recipe or ingredients.
        """
        user = request.user
        cart = self.get_cart(user)

        if ingredient_id:
            try:
                # Find the CartIngredient entry (ingredient in the cart)
                cart_ingredient = CartIngredient.objects.get(cart=cart, id=ingredient_id)
                cart_ingredient.delete()  # Remove the entry from the cart
                return Response({"message": "Ingredient removed from cart."}, status=status.HTTP_200_OK)
            except CartIngredient.DoesNotExist:
                return Response({"message": "Ingredient not found in cart."}, status=status.HTTP_404_NOT_FOUND)
        else:
            # If no ingredient ID is provided, clear all items in the cart
            cart.ingredients.all().delete()  # Remove all ingredients in the cart
            return Response({"message": "All ingredients removed from cart."}, status=status.HTTP_200_OK)


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



# UserIngredients Views
class UserIngredientsListCreateView(generics.ListCreateAPIView):
    queryset = UserIngredients.objects.all()
    serializer_class = UserIngredientsSerializer

class UserIngredientsDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserIngredients.objects.all()
    serializer_class = UserIngredientsSerializer


















@api_view(['GET'])
def upload_recipes_csv(request):
    # Path to your CSV file (ensure it's correct)
    file_path = 'updated_data.csv'  # Directly reference the CSV in the root directory
    # Call the utility function to upload recipes
    success, message = upload_recipes_from_csv(file_path)

    if success:
        return Response({'message': message}, status=status.HTTP_201_CREATED)
    else:
        return Response({'error': message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def weekly_meal_plan_view(request):
    user = request.user  # Get the logged-in user
    today = datetime.today().date()

    # Initialize response data
    weekly_plan = []

    # Loop through the next 7 days
    for i in range(7):
        plan_date = today + timedelta(days=i)

        # Retrieve the day plan for this date
        day_plan = DayPlan.objects.filter(user=user, date=plan_date).first()
        if day_plan:
            # Serialize the recipes in the day plan
            recipes = DayPlanRecipes.objects.filter(day_plan=day_plan).select_related('recipe')
            recipe_data = [
                {
                    'id': recipe.recipe.id,
                    'title': recipe.recipe.title,
                    'meal_type': recipe.recipe.meal_type,
                    'total_calories': recipe.recipe.total_calories,
                }
                for recipe in recipes
            ]

            # Add the day's plan to the weekly plan
            weekly_plan.append({
                'date': plan_date.strftime('%Y-%m-%d'),  # Convert date to string
                'recipes': recipe_data,
            })

    return Response({"weekly_plan": weekly_plan})

@api_view(['GET'])
def get_planned_recipes(request):
    """
    Retrieve all planned recipes for the authenticated user, grouped by day.
    """
    user = request.user  # Ensure the user is authenticated

    # Get today's date and the next 6 days
    today = datetime.today().date()
    end_date = today + timedelta(days=6)

    # Query all planned recipes for the user within the 7-day range
    plans = DayPlanRecipes.objects.filter(
        day_plan__user=user,
        day_plan__date__range=(today, end_date)
    ).select_related('day_plan', 'recipe')

    # Group recipes by day
    planned_recipes = {}
    for plan in plans:
        plan_date = plan.day_plan.date.strftime('%Y-%m-%d')  # Convert date to string
        if plan_date not in planned_recipes:
            planned_recipes[plan_date] = []
        planned_recipes[plan_date].append(RecipeSerializer(plan.recipe).data)

    # Format the response
    return Response({
        "planned_recipes": planned_recipes
    })