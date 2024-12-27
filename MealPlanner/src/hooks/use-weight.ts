import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { weightService } from '../services/weight-service'

export function useWeightHistory() {
  return useQuery({
    queryKey: ['weight'],
    queryFn: weightService.getWeightHistory
  })
}

export function useAddWeight() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (weight: number) => weightService.addWeightEntry(weight),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['weight'] })
    }
  })
}

