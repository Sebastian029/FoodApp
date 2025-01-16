from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    RecipeDetailView, IngredientListCreateView,
    UserNutrientPreferencesView,UserDislikedIngredientsView,
    RecipeListView, RecipeTypeView,
    UpdateWeightView, CanUpdateWeightView,
    CartAPIView, WeeklyMealPlanView,
    ResetMealPlansView, UserWeightListView,
    DietTypeView, DietChoicesView,
    NutrientSummaryView, WeeklyNutritionView,
    DayPlanItemView, RegisterView,
    CustomTokenObtainPairView,
    LogoutView, ProtectedView
)

from .views import upload_recipes_csv

urlpatterns = [
  # auth
  path('register/', RegisterView.as_view(), name='register'),
  path('login/', CustomTokenObtainPairView.as_view(), name='login'),
  path('logout/', LogoutView.as_view(), name='logout'),
  path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
  path('protected/', ProtectedView.as_view(), name='protected_view'),
  
  # home
  path('recipes/', RecipeListView.as_view(), name='recipe-list'),
  path('recipes/by-type/', RecipeTypeView.as_view(), name='recipe-by-type'),
  path('recipes/<int:pk>/', RecipeDetailView.as_view(), name='recipe-detail'),
  
  #planner
  path('weekly-meal-plan/', WeeklyMealPlanView.as_view(), name='weekly_meal_plan'),
  path('reset-meal-plans/', ResetMealPlansView.as_view(), name='reset-meal-plans'),
  path('nutrient-summary/', NutrientSummaryView.as_view(), name='nutrient-summary'),

  #planner/daily_items
  path('day-plan-items/', DayPlanItemView.as_view(), name='day-plan-items'),
  path('day-plan-items/<int:item_id>/', DayPlanItemView.as_view(), name='delete-day-plan-item'),
  path('weekly-plan/items/<int:item_id>/', DayPlanItemView.as_view(), name='update_item_quantity'),

  #cart
  path('cart/', CartAPIView.as_view(), name='cart_api'),
  path('cart/<int:ingredient_id>/', CartAPIView.as_view(), name='cart-ingredient'), 
  
  # user 
  path('can-update-weight/', CanUpdateWeightView.as_view(), name='can-update-weight'),
  path('update-weight/', UpdateWeightView.as_view(), name='update-weight'),
  path('weights/', UserWeightListView.as_view(), name='user-weight-list'),
  
  # user/update_diet_restrictions
  path('diet-type/', DietTypeView.as_view(), name='user-diet-type'),
  path('diet-choices/', DietChoicesView.as_view(), name='user-diet-choices'),
  path('ingredients/', IngredientListCreateView.as_view(), name='ingredient-list'),
  path('disliked-ingredients/', UserDislikedIngredientsView.as_view(), name='user-disliked-ingredients'),
  path('preferences/', UserNutrientPreferencesView.as_view(), name='user-nutrient-preferences'),
  
  
  #user/weekly_info
  path('weekly-nutrition/', WeeklyNutritionView.as_view(), name='weekly-nutrition'),
  
  # UPLOAD DATA
  path('upload-recipes/', upload_recipes_csv, name='upload-recipes'),
]
