import { useEffect } from 'react'
import { QueryClientProvider } from '@tanstack/react-query'
import { queryClient } from '../config/query-client'
import NetInfo from '@react-native-community/netinfo'
import { syncService } from '../services/sync-service'

export function CacheProvider({ children }: { children: React.ReactNode }) {
  useEffect(() => {
    // Listen for network status changes
    const unsubscribe = NetInfo.addEventListener(state => {
      if (state.isConnected) {
        // Try to sync pending changes when back online
        syncService.syncPendingChanges()
      }
    })

    return () => unsubscribe()
  }, [])

  return (
    <QueryClientProvider client={queryClient}>
      {children}
    </QueryClientProvider>
  )
}

