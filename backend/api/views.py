# api/views.py
from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import RegisterSerializer
from .models import (User, Recipe, Ingredient, RecipeIngredients,
                     DayPlan, DayPlanRecipes, RatedRecipes, UserWeight,
                     DislikedIngredients, UserIngredients, UserNutrientPreferences
)
from .serializers import (
    UserSerializer, RecipeSerializer, IngredientSerializer, 
    RecipeIngredientsSerializer, DayPlanSerializer, DayPlanRecipesSerializer, 
    RatedRecipesSerializer, UserWeightSerializer, DislikedIngredientsSerializer, 
    UserIngredientsSerializer, UserNutrientPreferencesSerializer
)
from .utils import select_meals, upload_recipes_from_csv


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
    file_path = 'data.csv'  # Directly reference the CSV in the root directory

    # Call the utility function to upload recipes
    success, message = upload_recipes_from_csv(file_path)

    if success:
        return Response({'message': message}, status=status.HTTP_201_CREATED)
    else:
        return Response({'error': message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def meal_selection_view(request):
    selected_meals = select_meals()
    serializer = RecipeSerializer(selected_meals, many=True)
    return Response({"selected_meals": serializer.data})
