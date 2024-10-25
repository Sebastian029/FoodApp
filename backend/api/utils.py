import pandas as pd
from pulp import LpProblem, LpVariable, lpSum, LpMaximize, LpMinimize
from .models import Recipe

def select_meals(optimize_field='protein', objective='maximize'):
    # Query relevant data from the Recipe model and convert to a DataFrame
    recipes = Recipe.objects.all().values('id', 'title', 'total_calories', 'sugars', 'protein', 'iron', 'potassium', 'meal_type')
    df = pd.DataFrame(list(recipes))

    # Convert string fields to numeric for calculations
    df['total_calories'] = pd.to_numeric(df['total_calories'], errors='coerce')
    df['sugars'] = pd.to_numeric(df['sugars'], errors='coerce')
    df['protein'] = pd.to_numeric(df['protein'], errors='coerce')
    df['iron'] = pd.to_numeric(df['iron'], errors='coerce')
    df['potassium'] = pd.to_numeric(df['potassium'], errors='coerce')

    # Drop rows with NaN values in key columns (optional, depends on data quality)
    df = df.dropna(subset=['total_calories', 'sugars', 'protein', 'iron', 'potassium'])

    # Define the optimization problem
    model = LpProblem("Meal_Selection", LpMaximize if objective == 'maximize' else LpMinimize)

    # Define decision variables (one binary variable per meal)
    meal_vars = [LpVariable(f"meal_{i}", cat='Binary') for i in df.index]

    # Objective function: optimize the specified field
    if optimize_field in df.columns:
        model += lpSum(df.loc[i, optimize_field] * meal_vars[i] for i in df.index), f"{objective.capitalize()}_{optimize_field.capitalize()}"

    # Nutritional constraints with ranges
    model += lpSum(df.loc[i, 'total_calories'] * meal_vars[i] for i in df.index) >= 0, "Min_Calories"
    model += lpSum(df.loc[i, 'total_calories'] * meal_vars[i] for i in df.index) <= 10000, "Max_Calories"
    
    model += lpSum(df.loc[i, 'sugars'] * meal_vars[i] for i in df.index) >= 0, "Min_Sugars"  # Add your minimum limit here
    model += lpSum(df.loc[i, 'sugars'] * meal_vars[i] for i in df.index) <= 50, "Max_Sugars"

    model += lpSum(df.loc[i, 'iron'] * meal_vars[i] for i in df.index) >= 18, "Min_Iron"
    model += lpSum(df.loc[i, 'iron'] * meal_vars[i] for i in df.index) <= 50, "Max_Iron"  # Adjust this value as needed
    
    model += lpSum(df.loc[i, 'potassium'] * meal_vars[i] for i in df.index) >= 3500, "Min_Potassium"
    model += lpSum(df.loc[i, 'potassium'] * meal_vars[i] for i in df.index) <= 5000, "Max_Potassium"  # Adjust this value as needed

    model += lpSum(df.loc[i, 'protein'] * meal_vars[i] for i in df.index) >= 50, "Min_Protein"
    model += lpSum(df.loc[i, 'protein'] * meal_vars[i] for i in df.index) <= 200, "Max_Protein"  # Adjust this value as needed

    # Constraint to limit the number of selected meals to a maximum of 6
    model += lpSum(meal_vars) <= 6, "Max_Meals"

    # Constraints to ensure at least one meal from each category
    for meal_type in ['lunch', 'dinner', 'snack', 'breakfast']:
        indices = df.index[df['meal_type'] == meal_type].tolist()
        model += lpSum(meal_vars[i] for i in indices) >= 1, f"At_Least_One_{meal_type.capitalize()}"

    # Solve the model
    model.solve()

    # Gather selected meal IDs, ensuring each is selected only once
    selected_ids = list(set([df.loc[i, 'id'] for i in df.index if meal_vars[i].varValue == 1]))

    # Query the actual Recipe objects for these selected IDs
    selected_meals = Recipe.objects.filter(id__in=selected_ids)

    # Print summary of total nutritional values for selected meals
    total_calories = sum(df.loc[i, 'total_calories'] * meal_vars[i].varValue for i in df.index)
    total_sugars = sum(df.loc[i, 'sugars'] * meal_vars[i].varValue for i in df.index)
    total_protein = sum(df.loc[i, 'protein'] * meal_vars[i].varValue for i in df.index)
    total_iron = sum(df.loc[i, 'iron'] * meal_vars[i].varValue for i in df.index)
    total_potassium = sum(df.loc[i, 'potassium'] * meal_vars[i].varValue for i in df.index)

    print("Nutritional Summary of Selected Meals:")
    print(f"Total Calories: {total_calories:.2f}")
    print(f"Total Sugars: {total_sugars:.2f}")
    print(f"Total Protein: {total_protein:.2f}")
    print(f"Total Iron: {total_iron:.2f}")
    print(f"Total Potassium: {total_potassium:.2f}")

    return selected_meals
