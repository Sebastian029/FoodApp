import AsyncStorage from '@react-native-async-storage/async-storage'

const TOKEN_KEY = '@MealPlanner:token'

export const tokenManager = {
  async setToken(token) {
    try {
      await AsyncStorage.setItem(TOKEN_KEY, token)
    } catch (error) {
      console.error('Error saving token:', error)
    }
  },

  async getToken() {
    try {
      return await AsyncStorage.getItem(TOKEN_KEY)
    } catch (error) {
      console.error('Error getting token:', error)
      return null
    }
  },

  async removeToken() {
    try {
      await AsyncStorage.removeItem(TOKEN_KEY)
    } catch (error) {
      console.error('Error removing token:', error)
    }
  }
}

