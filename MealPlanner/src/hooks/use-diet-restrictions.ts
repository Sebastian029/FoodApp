import { useState, useCallback } from 'react'
import { dietService, DietRestrictions, WeightEntry } from '../services/diet-service'

export function useDietRestrictions() {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [restrictions, setRestrictions] = useState<DietRestrictions | null>(null)
  const [weightHistory, setWeightHistory] = useState<WeightEntry[]>([])

  const fetchRestrictions = useCallback(async () => {
    try {
      setLoading(true)
      setError(null)
      const data = await dietService.getDietRestrictions()
      setRestrictions(data)
    } catch (err) {
      setError('Failed to load diet restrictions')
      throw err
    } finally {
      setLoading(false)
    }
  }, [])

  const updateRestrictions = useCallback(async (data: DietRestrictions) => {
    try {
      setLoading(true)
      setError(null)
      const updated = await dietService.updateDietRestrictions(data)
      setRestrictions(updated)
    } catch (err) {
      setError('Failed to update diet restrictions')
      throw err
    } finally {
      setLoading(false)
    }
  }, [])

  const fetchWeightHistory = useCallback(async () => {
    try {
      setLoading(true)
      setError(null)
      const data = await dietService.getWeightHistory()
      setWeightHistory(data)
    } catch (err) {
      setError('Failed to load weight history')
      throw err
    } finally {
      setLoading(false)
    }
  }, [])

  const addWeightEntry = useCallback(async (weight: number) => {
    try {
      setLoading(true)
      setError(null)
      await dietService.addWeightEntry(weight)
      await fetchWeightHistory()
    } catch (err) {
      setError('Failed to add weight entry')
      throw err
    } finally {
      setLoading(false)
    }
  }, [fetchWeightHistory])

  return {
    restrictions,
    weightHistory,
    loading,
    error,
    fetchRestrictions,
    updateRestrictions,
    fetchWeightHistory,
    addWeightEntry
  }
}

