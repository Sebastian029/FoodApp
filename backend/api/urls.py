# api/urls.py
from django.urls import path
from .views import (
    UserListCreateView, UserDetailView, RecipeListCreateView, RecipeDetailView, 
    IngredientListCreateView, RecipeIngredientsListCreateView, 
    RecipeIngredientsDetailView, DayPlanListCreateView, DayPlanDetailView, DayPlanRecipesListCreateView, 
    DayPlanRecipesDetailView, RatedRecipesListCreateView, RatedRecipesDetailView, UserWeightListCreateView, 
    UserWeightDetailView,
    UserIngredientsListCreateView, UserIngredientsDetailView, UserNutrientPreferencesView,
    UserDislikedIngredientsView, RecipeListView, RecipeTypeView, UpdateWeightView, CanUpdateWeightView,
    CartAPIView, WeeklyMealPlanView, ResetMealPlansView, UserWeightListView, DietTypeView, DietChoicesView, NutrientSummaryView, WeeklyNutritionView, DayPlanItemView
)

from .views import upload_recipes_csv
from .views import RegisterView, CustomTokenObtainPairView, LogoutView
from .views import ProtectedView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('protected/', ProtectedView.as_view(), name='protected_view'),
    path('users/', UserListCreateView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('preferences/', UserNutrientPreferencesView.as_view(), name='user-nutrient-preferences'),
    path('ingredients/', IngredientListCreateView.as_view(), name='ingredient-list'),
    path('disliked-ingredients/', UserDislikedIngredientsView.as_view(), name='user-disliked-ingredients'),

    path('recipes/by-type/', RecipeTypeView.as_view(), name='recipe-by-type'),
    path('recipes/', RecipeListView.as_view(), name='recipe-list'),
    path('recipes/<int:pk>/', RecipeDetailView.as_view(), name='recipe-detail'),
    path('can-update-weight/', CanUpdateWeightView.as_view(), name='can-update-weight'),
    path('update-weight/', UpdateWeightView.as_view(), name='update-weight'),
    path('cart/', CartAPIView.as_view(), name='cart_api'),
    path('cart/<int:ingredient_id>/', CartAPIView.as_view(), name='cart-ingredient'), 
    path('weights/', UserWeightListView.as_view(), name='user-weight-list'),
    path('diet-type/', DietTypeView.as_view(), name='user-diet-type'),
    path('diet-choices/', DietChoicesView.as_view(), name='user-diet-choices'),
    path('nutrient-summary/', NutrientSummaryView.as_view(), name='nutrient-summary'),
    path('weekly-nutrition/', WeeklyNutritionView.as_view(), name='weekly-nutrition'),
    path('day-plan-items/', DayPlanItemView.as_view(), name='day-plan-items'),
    path('day-plan-items/<int:item_id>/', DayPlanItemView.as_view(), name='delete-day-plan-item'),
    path('weekly-plan/items/<int:item_id>/', DayPlanItemView.as_view(), name='update_item_quantity'),
  

    path('recipe-ingredients/', RecipeIngredientsListCreateView.as_view(), name='recipeingredients-list'),
    path('recipe-ingredients/<int:pk>/', RecipeIngredientsDetailView.as_view(), name='recipeingredients-detail'),

    path('day-plans/', DayPlanListCreateView.as_view(), name='dayplan-list'),
    path('day-plans/<int:pk>/', DayPlanDetailView.as_view(), name='dayplan-detail'),

    path('day-plan-recipes/', DayPlanRecipesListCreateView.as_view(), name='dayplanrecipes-list'),
    path('day-plan-recipes/<int:pk>/', DayPlanRecipesDetailView.as_view(), name='dayplanrecipes-detail'),

    path('rated-recipes/', RatedRecipesListCreateView.as_view(), name='ratedrecipes-list'),
    path('rated-recipes/<int:pk>/', RatedRecipesDetailView.as_view(), name='ratedrecipes-detail'),

    path('user-weight/', UserWeightListCreateView.as_view(), name='userweight-list'),
    path('user-weight/<int:pk>/', UserWeightDetailView.as_view(), name='userweight-detail'),



    path('user-ingredients/', UserIngredientsListCreateView.as_view(), name='useringredients-list'),
    path('user-ingredients/<int:pk>/', UserIngredientsDetailView.as_view(), name='useringredients-detail'),
    
    path('upload-recipes/', upload_recipes_csv, name='upload-recipes'),
    #path('plan_meals/', meal_selection_view, name='select_meals'),
    
    path('weekly-meal-plan/', WeeklyMealPlanView.as_view(), name='weekly_meal_plan'),
    path('reset-meal-plans/', ResetMealPlansView.as_view(), name='reset-meal-plans'),

  #  path('planned-recipes/', get_planned_recipes, name='planned_recipes'),


]
