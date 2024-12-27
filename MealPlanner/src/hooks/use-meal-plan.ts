import { useState, useCallback } from 'react'
import { mealsService, MealPlan } from '../services/meals-service'

export function useMealPlan() {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [mealPlan, setMealPlan] = useState<MealPlan | null>(null)

  const fetchMealPlan = useCallback(async (date: string) => {
    try {
      setLoading(true)
      setError(null)
      const data = await mealsService.getMealPlan(date)
      setMealPlan(data)
    } catch (err) {
      setError('Failed to load meal plan')
      throw err
    } finally {
      setLoading(false)
    }
  }, [])

  const rateMeal = useCallback(async (id: string, rating: number) => {
    try {
      setLoading(true)
      setError(null)
      await mealsService.rateMeal(id, rating)
      // Refresh meal plan after rating
      if (mealPlan) {
        await fetchMealPlan(mealPlan.date)
      }
    } catch (err) {
      setError('Failed to rate meal')
      throw err
    } finally {
      setLoading(false)
    }
  }, [mealPlan, fetchMealPlan])

  return {
    mealPlan,
    loading,
    error,
    fetchMealPlan,
    rateMeal
  }
}

