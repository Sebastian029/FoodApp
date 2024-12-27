import type { ApiResponse, WeightEntry } from '../types/api'
import apiClient from './api-client'

export const weightService = {
  async getWeightHistory(): Promise<ApiResponse<WeightEntry[]>> {
    const { data } = await apiClient.get('/weight/history')
    return data
  },

  async addWeightEntry(weight: number): Promise<ApiResponse<WeightEntry>> {
    const { data } = await apiClient.post('/weight', { weight })
    return data
  }
}

