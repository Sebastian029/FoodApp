import { useQuery, useMutation } from '@tanstack/react-query'
import { dietService } from '../services/diet-service'
import { storage } from '../utils/storage'

export function useDietRestrictions() {
  return useQuery({
    queryKey: ['dietRestrictions'],
    queryFn: async () => {
      try {
        const data = await dietService.getDietRestrictions()
        await storage.set('dietRestrictions', data)
        return data
      } catch (error) {
        const cached = await storage.get('dietRestrictions')
        if (cached) {
          return cached
        }
        throw error
      }
    },
    // Keep cached data for longer since it changes less frequently
    staleTime: 1000 * 60 * 60, // 1 hour
  })
}

export function useUpdateDietRestrictions() {
  return useMutation({
    mutationFn: async (restrictions: any) => {
      try {
        const result = await dietService.updateDietRestrictions(restrictions)
        await storage.set('dietRestrictions', result)
        return result
      } catch (error) {
        // Store failed updates for retry
        await storage.set('pendingDietUpdate', restrictions)
        throw error
      }
    }
  })
}

