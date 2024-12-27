export interface ApiResponse<T> {
  data: T;
  message: string;
  status: number;
}

export interface Meal {
  id: string;
  name: string;
  description: string;
  calories: number;
  proteins: number;
  carbs: number;
  fats: number;
  ingredients: Ingredient[];
  preparation: string[];
  rating?: number;
}

export interface Ingredient {
  id: string;
  name: string;
  amount: number;
  unit: string;
}

export interface WeightEntry {
  id: string;
  weight: number;
  date: string;
}

export interface DietRestrictions {
  calories: { min: number; max: number };
  proteins: { min: number; max: number };
  fiber: { min: number; max: number };
  sugar: { min: number; max: number };
  dietType?: string;
  blockedIngredients: string[];
}

