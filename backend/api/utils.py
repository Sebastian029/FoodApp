import pandas as pd
from pulp import LpProblem, LpVariable, lpSum, LpMaximize, LpMinimize, PULP_CBC_CMD
from django.conf import settings
from api.models import Recipe, Ingredient, RecipeIngredients, DislikedIngredients, UserNutrientPreferences
from django.contrib.auth import get_user_model
import csv
from django.db import transaction




# api/utils.py
from datetime import datetime, timedelta
from .models import DayPlan, DayPlanRecipes, UserRecipeUsage

def plan_meals_for_week(user):
    today = datetime.today().date()
    used_recipe_ids = DayPlanRecipes.objects.filter(
        day_plan__user=user
    ).values_list('recipe_id', flat=True)

    for i in range(7):
        plan_date = today + timedelta(days=i)

        # Get or create a DayPlan for the specific date
        day_plan, created = DayPlan.objects.get_or_create(user=user, date=plan_date)

        # Skip if the day already has enough recipes (e.g., 3 per day)
        if DayPlanRecipes.objects.filter(day_plan=day_plan).count() >= 3:
            continue

        # Select meals for the day
        selected_recipes = select_meals(user, excluded_ids=used_recipe_ids)

        # Add selected recipes to the DayPlan and update usage
        for recipe in selected_recipes:
            if not DayPlanRecipes.objects.filter(day_plan=day_plan, recipe=recipe).exists():
                DayPlanRecipes.objects.create(day_plan=day_plan, recipe=recipe)

                # Update or create a UserRecipeUsage record
                UserRecipeUsage.objects.update_or_create(
                    user=user,
                    recipe=recipe,
                    defaults={'last_used': today}
                )



def select_meals(user, optimize_field='protein', objective='maximize', excluded_ids=[]):
    user_preferences = UserNutrientPreferences.objects.get(user=user)
    diet_type = user_preferences.diet_type

    if diet_type == 'low_calories':
        optimize_field = 'total_calories'
        objective = 'minimize'
    elif diet_type == 'high_calories':
        optimize_field = 'total_calories'
        objective = 'maximize'
    elif diet_type.startswith('low_') or diet_type.startswith('high_'):
        nutrient = diet_type.split('_', 1)[1]
        
        valid_nutrients = ['protein', 'fat', 'carbohydrates', 'fiber', 'sugars', 'iron', 'potassium']
        if nutrient in valid_nutrients:
            optimize_field = nutrient
            objective = 'minimize' if diet_type.startswith('low_') else 'maximize'
    
    
    
    preferences, created = UserNutrientPreferences.objects.get_or_create(
        user=user,
        defaults={
            'min_protein': 0,
            'max_protein': 0,
            'min_fat': 0,
            'max_fat': 0,
            'min_carbohydrates': 0,
            'max_carbohydrates': 0,
            'min_fiber': 0,
            'max_fiber': 0,
            'min_calories': 1500,
            'max_calories': 2500,
            'min_sugars': 0,
            'max_sugars': 0,
            'min_iron': 0,
            'max_iron': 0,
            'min_potassium': 0,
            'max_potassium': 0
        }
    )

    # Get list of disliked ingredients for the user
    disliked_ingredients = DislikedIngredients.objects.filter(user=user).values_list('ingredient_id', flat=True)

    
   

    # Filter recipes, excluding only the remaining IDs
    recipes = Recipe.objects.exclude(
        recipeingredients__ingredient__in=disliked_ingredients
    ).exclude(
        id__in=excluded_ids
    ).values(
        'id', 'title', 'total_calories', 'sugars', 'protein', 'fat', 'carbohydrates', 'fiber', 'iron', 'potassium', 'meal_type'
    )

    # Convert recipes into a pandas DataFrame
    df = pd.DataFrame(list(recipes))

    # If no recipes are available after filtering, return an empty QuerySet
    if df.empty:
        return Recipe.objects.none()

    # Convert string fields to numeric for calculations
    for field in ['total_calories', 'sugars', 'protein','fat','carbohydrates','fiber', 'iron', 'potassium']:
        df[field] = pd.to_numeric(df[field], errors='coerce')

    # Drop rows with NaN values in key columns
    df.dropna(subset=['total_calories', 'sugars', 'protein','fat','carbohydrates','fiber', 'iron', 'potassium'], inplace=True)

    # Set up the optimization problem
    model = LpProblem("Meal_Selection", LpMaximize if objective == 'maximize' else LpMinimize)

    # Define decision variables for each meal
    meal_vars = [LpVariable(f"meal_{i}", cat='Binary') for i in df.index]

    # Limit the number of selected meals to a maximum of 6
    model += lpSum(meal_vars) <= 6, "Max_Meals"
    
    model += lpSum(
        2 * df.loc[i, 'total_calories'] * meal_vars[i]  
        + 1 * df.loc[i, 'protein'] * meal_vars[i]              
        - 0.5 * df.loc[i, 'sugars'] * meal_vars[i]       
        for i in df.index
    ), "Weighted_Nutrient_Optimization"
    
    # Objective function
    if optimize_field in df.columns:
        model += lpSum(df.loc[i, optimize_field] * meal_vars[i] for i in df.index), f"{objective.capitalize()}_{optimize_field.capitalize()}"


    if preferences.min_calories > 0 and preferences.max_calories > 0:
        model += lpSum(df.loc[i, 'total_calories'] * meal_vars[i] for i in df.index) >= preferences.min_calories, "Min_Calories"
        model += lpSum(df.loc[i, 'total_calories'] * meal_vars[i] for i in df.index) <= preferences.max_calories, "Max_Calories"
    
    if preferences.min_sugars > 0 and preferences.max_sugars > 0:
        model += lpSum(df.loc[i, 'sugars'] * meal_vars[i] for i in df.index) >= preferences.min_sugars, "Min_Sugars"
        model += lpSum(df.loc[i, 'sugars'] * meal_vars[i] for i in df.index) <= preferences.max_sugars, "Max_Sugars"
    
    if preferences.min_iron > 0 and preferences.max_iron > 0:
        model += lpSum(df.loc[i, 'iron'] * meal_vars[i] for i in df.index) >= preferences.min_iron, "Min_Iron"
        model += lpSum(df.loc[i, 'iron'] * meal_vars[i] for i in df.index) <= preferences.max_iron, "Max_Iron"
    
    if preferences.min_potassium > 0 and preferences.max_potassium > 0:
        model += lpSum(df.loc[i, 'potassium'] * meal_vars[i] for i in df.index) >= preferences.min_potassium, "Min_Potassium"
        model += lpSum(df.loc[i, 'potassium'] * meal_vars[i] for i in df.index) <= preferences.max_potassium, "Max_Potassium"
    
    if preferences.min_protein > 0 and preferences.max_protein > 0:
        model += lpSum(df.loc[i, 'protein'] * meal_vars[i] for i in df.index) >= preferences.min_protein, "Min_Protein"
        model += lpSum(df.loc[i, 'protein'] * meal_vars[i] for i in df.index) <= preferences.max_protein, "Max_Protein"
    
    if preferences.min_fat > 0 and preferences.max_fat > 0:
        model += lpSum(df.loc[i, 'fat'] * meal_vars[i] for i in df.index) >= preferences.min_fat, "Min_Fat"
        model += lpSum(df.loc[i, 'fat'] * meal_vars[i] for i in df.index) <= preferences.max_fat, "Max_Fat"
    
    if preferences.min_carbohydrates > 0 and preferences.max_carbohydrates > 0:
        model += lpSum(df.loc[i, 'carbohydrates'] * meal_vars[i] for i in df.index) >= preferences.min_carbohydrates, "Min_Carbohydrates"
        model += lpSum(df.loc[i, 'carbohydrates'] * meal_vars[i] for i in df.index) <= preferences.max_carbohydrates, "Max_Carbohydrates"
    
    if preferences.min_fiber > 0 and preferences.max_fiber > 0:
        model += lpSum(df.loc[i, 'fiber'] * meal_vars[i] for i in df.index) >= preferences.min_fiber, "Min_Fiber"
        model += lpSum(df.loc[i, 'fiber'] * meal_vars[i] for i in df.index) <= preferences.max_fiber, "Max_Fiber"
    

    # Ensure at least one meal from each category
    for meal_type in ['lunch', 'dinner', 'snack', 'breakfast']:
        indices = df.index[df['meal_type'] == meal_type].tolist()
        if indices:
            model += lpSum(meal_vars[i] for i in indices) >= 1, f"At_Least_One_{meal_type.capitalize()}"

    # Solve the model
    model.solve(PULP_CBC_CMD(msg=False))

    # Gather selected meal IDs
    selected_ids = [df.loc[i, 'id'] for i in df.index if meal_vars[i].varValue == 1]

    # Query the actual Recipe objects for these selected IDs
    selected_meals = Recipe.objects.filter(id__in=selected_ids)

    # Return the selected meals
    return selected_meals


    



def upload_recipes_from_csv(file_path):
    try:
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')

            # Use a transaction to ensure atomicity
            with transaction.atomic():
                for row in reader:
                    # Prepare data for Recipe creation
                    recipe_data = {
                        'title': row['name'],
                        'description': row['short_description'],
                        'total_calories': row['total_calories'],
                        'carbohydrates': row['carbohydrates'],
                        'fat': row['fat'],
                        'fiber': row['fiber'],
                        'sugars': row['sugars'],
                        'protein': row['protein'],
                        'iron': row['iron'],
                        'potassium': row['potassium'],
                        'preparation_time': int(row['preparation_time']),
                        'preparation_guide': row['preparation_guide'],
                        'meal_type': row['meal_type'],
                    }

                    # Create the Recipe object
                    recipe = Recipe.objects.create(**recipe_data)

                    # Handle ingredients if they exist
                    if 'ingredients' in row:
                        # Assuming 'ingredients' column has data like: "Flour:2 cups, Sugar:1 cup"
                        ingredients = row['ingredients'].split(',')
                        for ingredient_entry in ingredients:
                            # Split ingredient name, quantity, and unit
                            try:
                                name, quantity_unit = ingredient_entry.split(':', 1)
                                quantity, unit = quantity_unit.strip().split(' ', 1)
                            except ValueError:
                                # If format is invalid, use default values
                                name = ingredient_entry.strip()
                                quantity = 0.0  # Default quantity
                                unit = ""       # Default unit

                            # Trim and validate data
                            name = name.strip()
                            quantity = float(quantity)
                            unit = unit.strip()

                            # Check if ingredient exists or create it
                            ingredient_obj, created = Ingredient.objects.get_or_create(name=name)

                            # Create a relationship in the RecipeIngredients table
                            RecipeIngredients.objects.create(
                                recipe=recipe,
                                ingredient=ingredient_obj,
                                quantity=quantity,
                                unit=unit,
                            )

        return True, 'Recipes uploaded successfully!'
    except Exception as e:
        return False, str(e)
    
    