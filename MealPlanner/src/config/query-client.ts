import { QueryClient } from '@tanstack/react-query'
import { storage } from '../utils/storage'
import { AxiosError } from 'axios'

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5, // Data stays fresh for 5 minutes
      cacheTime: 1000 * 60 * 60 * 24, // Cache persists for 24 hours
      retry: 2,
      // Persist query data between app restarts
      gcTime: Infinity,
      // Use cached data while fetching
      keepPreviousData: true,
      // Handle offline scenarios
      networkMode: 'online',
      // Save query data to AsyncStorage
      async onSuccess(data, query) {
        await storage.set(`query_${query.queryKey.join('_')}`, data)
      },
      // Load from AsyncStorage if network request fails
      async onError(error: AxiosError, query) {
        if (error.message === 'Network Error') {
          const cached = await storage.get(`query_${query.queryKey.join('_')}`)
          if (cached) {
            return cached
          }
        }
      }
    },
    mutations: {
      // Retry failed mutations
      retry: 1,
      // Queue mutations when offline
      networkMode: 'online',
    },
  },
})

