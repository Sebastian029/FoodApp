import { storage } from '../utils/storage'
import { mealsService } from './meals-service'
import { dietService } from './diet-service'
import NetInfo from '@react-native-community/netinfo'

export const syncService = {
  async syncPendingChanges() {
    const isConnected = (await NetInfo.fetch()).isConnected

    if (!isConnected) {
      return
    }

    try {
      // Sync pending meal ratings
      const pendingRatings = await storage.get('pendingRatings')
      if (pendingRatings?.length) {
        for (const { mealId, rating } of pendingRatings) {
          await mealsService.rateMeal(mealId, rating)
        }
        await storage.remove('pendingRatings')
      }

      // Sync pending diet restrictions update
      const pendingDietUpdate = await storage.get('pendingDietUpdate')
      if (pendingDietUpdate) {
        await dietService.updateDietRestrictions(pendingDietUpdate)
        await storage.remove('pendingDietUpdate')
      }
    } catch (error) {
      console.error('Sync failed:', error)
    }
  }
}

