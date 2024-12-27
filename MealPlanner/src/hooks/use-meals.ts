import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { mealsService } from '../services/meals-service'

export function useDailyMeals(date: string) {
  return useQuery({
    queryKey: ['meals', date],
    queryFn: () => mealsService.getDailyMeals(date)
  })
}

export function useMeal(id: string) {
  return useQuery({
    queryKey: ['meal', id],
    queryFn: () => mealsService.getMealById(id)
  })
}

export function useRateMeal() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({ id, rating }: { id: string; rating: number }) => 
      mealsService.rateMeal(id, rating),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['meals'] })
    }
  })
}

