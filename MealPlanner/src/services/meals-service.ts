import axios from '../config/axios-config'

export interface Meal {
  id: string
  name: string
  description: string
  calories: number
  protein: number
  carbs: number
  fat: number
  rating?: number
}

export interface MealPlan {
  date: string
  meals: {
    breakfast: Meal[]
    lunch: Meal[]
    dinner: Meal[]
  }
}

export const mealsService = {
  async getMealPlan(date: string): Promise<MealPlan> {
    const response = await axios.get<MealPlan>(`/meals/plan/${date}`)
    return response.data
  },

  async rateMeal(id: string, rating: number): Promise<Meal> {
    const response = await axios.post<Meal>(`/meals/${id}/rate`, { rating })
    return response.data
  },

  async updateMealPlan(date: string, mealPlan: MealPlan): Promise<MealPlan> {
    const response = await axios.put<MealPlan>(`/meals/plan/${date}`, mealPlan)
    return response.data
  }
}

