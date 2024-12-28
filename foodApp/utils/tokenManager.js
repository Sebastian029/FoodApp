import AsyncStorage from "@react-native-async-storage/async-storage";

const ACCESS_TOKEN_KEY = "@MealPlanner:accessToken";
const REFRESH_TOKEN_KEY = "@MealPlanner:refreshToken";

export const tokenManager = {
  async setTokens(tokens) {
    try {
      await AsyncStorage.multiSet([
        [ACCESS_TOKEN_KEY, tokens.access],
        [REFRESH_TOKEN_KEY, tokens.refresh],
      ]);
    } catch (error) {
      console.error("Error saving tokens:", error);
    }
  },

  async getAccessToken() {
    try {
      return await AsyncStorage.getItem(ACCESS_TOKEN_KEY);
    } catch (error) {
      console.error("Error getting access token:", error);
      return null;
    }
  },

  async getRefreshToken() {
    try {
      return await AsyncStorage.getItem(REFRESH_TOKEN_KEY);
    } catch (error) {
      console.error("Error getting refresh token:", error);
      return null;
    }
  },

  async removeTokens() {
    try {
      await AsyncStorage.multiRemove([ACCESS_TOKEN_KEY, REFRESH_TOKEN_KEY]);
    } catch (error) {
      console.error("Error removing tokens:", error);
    }
  },
};
