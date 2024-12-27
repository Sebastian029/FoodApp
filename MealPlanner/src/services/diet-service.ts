import axios from '../config/axios-config'

export interface DietRestrictions {
  calories: { min: number; max: number }
  proteins: { min: number; max: number }
  fiber: { min: number; max: number }
  sugar: { min: number; max: number }
  dietType?: string
  blockedIngredients: string[]
}

export interface WeightEntry {
  date: string
  weight: number
}

export const dietService = {
  async getDietRestrictions(): Promise<DietRestrictions> {
    const response = await axios.get<DietRestrictions>('/diet/restrictions')
    return response.data
  },

  async updateDietRestrictions(data: DietRestrictions): Promise<DietRestrictions> {
    const response = await axios.put<DietRestrictions>('/diet/restrictions', data)
    return response.data
  },

  async getWeightHistory(): Promise<WeightEntry[]> {
    const response = await axios.get<WeightEntry[]>('/weight/history')
    return response.data
  },

  async addWeightEntry(weight: number): Promise<WeightEntry> {
    const response = await axios.post<WeightEntry>('/weight', { weight })
    return response.data
  }
}

