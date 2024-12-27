import { useQuery, useMutation } from '@tanstack/react-query'
import { mealsService } from '../services/meals-service'
import { storage } from '../utils/storage'

export function useMealPlan(date: string) {
  return useQuery({
    queryKey: ['mealPlan', date],
    queryFn: async () => {
      try {
        const data = await mealsService.getMealPlan(date)
        // Cache successful response
        await storage.set(`mealPlan_${date}`, data)
        return data
      } catch (error) {
        // Try to load from cache if network request fails
        const cached = await storage.get(`mealPlan_${date}`)
        if (cached) {
          return cached
        }
        throw error
      }
    },
    // Keep cached data valid for 5 minutes
    staleTime: 1000 * 60 * 5,
  })
}

export function useRateMeal() {
  return useMutation({
    mutationFn: async ({ mealId, rating }: { mealId: string; rating: number }) => {
      try {
        const result = await mealsService.rateMeal(mealId, rating)
        // Update cache after successful rating
        const cached = await storage.get('recentMeals')
        if (cached) {
          const updated = cached.map((meal: any) =>
            meal.id === mealId ? { ...meal, rating } : meal
          )
          await storage.set('recentMeals', updated)
        }
        return result
      } catch (error) {
        // Queue failed mutations for retry
        const pendingRatings = await storage.get('pendingRatings') || []
        await storage.set('pendingRatings', [
          ...pendingRatings,
          { mealId, rating }
        ])
        throw error
      }
    }
  })
}

