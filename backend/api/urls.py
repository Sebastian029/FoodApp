# api/urls.py
from django.urls import path
from .views import (
    UserListCreateView, UserDetailView, RecipeListCreateView, RecipeDetailView, 
    IngredientListCreateView, IngredientDetailView, RecipeIngredientsListCreateView, 
    RecipeIngredientsDetailView, DayPlanListCreateView, DayPlanDetailView, DayPlanRecipesListCreateView, 
    DayPlanRecipesDetailView, RatedRecipesListCreateView, RatedRecipesDetailView, UserWeightListCreateView, 
    UserWeightDetailView, DislikedIngredientsListCreateView, DislikedIngredientsDetailView, 
    UserIngredientsListCreateView, UserIngredientsDetailView
)

from .views import upload_recipes_csv, meal_selection_view


urlpatterns = [
    path('users/', UserListCreateView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    
    path('recipes/', RecipeListCreateView.as_view(), name='recipe-list'),
    path('recipes/<int:pk>/', RecipeDetailView.as_view(), name='recipe-detail'),

    path('ingredients/', IngredientListCreateView.as_view(), name='ingredient-list'),
    path('ingredients/<int:pk>/', IngredientDetailView.as_view(), name='ingredient-detail'),

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

    path('disliked-ingredients/', DislikedIngredientsListCreateView.as_view(), name='dislikedingredients-list'),
    path('disliked-ingredients/<int:pk>/', DislikedIngredientsDetailView.as_view(), name='dislikedingredients-detail'),

    path('user-ingredients/', UserIngredientsListCreateView.as_view(), name='useringredients-list'),
    path('user-ingredients/<int:pk>/', UserIngredientsDetailView.as_view(), name='useringredients-detail'),
    
    path('upload-recipes/', upload_recipes_csv, name='upload-recipes'),
    path('plan_meals/', meal_selection_view, name='select_meals')
]
