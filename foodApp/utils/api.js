import axios from "axios";
import { tokenManager } from "./tokenManager";

const BASE_URL = "YOUR_API_URL";

const api = axios.create({
  baseURL: "http://192.168.0.177:8000/api",
  headers: {
    "Content-Type": "application/json",
  },
});

// Create a separate instance for refresh token requests
const refreshApi = axios.create({
  baseURL: BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// Track if we're refreshing the token
let isRefreshing = false;
let failedQueue = [];

const processQueue = (error, token = null) => {
  failedQueue.forEach((prom) => {
    if (error) {
      prom.reject(error);
    } else {
      prom.resolve(token);
    }
  });
  failedQueue = [];
};

// Add token to requests
api.interceptors.request.use(async (config) => {
  const token = await tokenManager.getAccessToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle token refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    // If error is not 401 or request has already been retried, reject
    if (error.response?.status !== 401 || originalRequest._retry) {
      return Promise.reject(error);
    }

    if (isRefreshing) {
      // If we're already refreshing, queue this request
      return new Promise((resolve, reject) => {
        failedQueue.push({ resolve, reject });
      })
        .then((token) => {
          originalRequest.headers.Authorization = `Bearer ${token}`;
          return api(originalRequest);
        })
        .catch((err) => Promise.reject(err));
    }

    originalRequest._retry = true;
    isRefreshing = true;

    try {
      const refreshToken = await tokenManager.getRefreshToken();
      const response = await refreshApi.post("/token/refresh/", {
        refresh: refreshToken,
      });

      const { access } = response.data;
      await tokenManager.setTokens({ access, refresh: refreshToken });

      // Update authorization header
      api.defaults.headers.common.Authorization = `Bearer ${access}`;
      originalRequest.headers.Authorization = `Bearer ${access}`;

      processQueue(null, access);
      return api(originalRequest);
    } catch (refreshError) {
      processQueue(refreshError, null);
      await tokenManager.removeTokens();
      // You might want to navigate to login screen here
      return Promise.reject(refreshError);
    } finally {
      isRefreshing = false;
    }
  }
);

export const authAPI = {
  login: async (credentials) => {
    const response = await api.post("/login/", credentials);
    await tokenManager.setTokens(response.data);
    return response;
  },
  register: async (userData) => {
    const response = await api.post("/register/", userData);
    await tokenManager.setTokens(response.data);
    return response;
  },
  logout: async () => {
    try {
      const refreshToken = await tokenManager.getRefreshToken();

      // If a refresh token exists, send it in the POST request
      if (refreshToken) {
        const response = await api.post("/logout/", { refresh: refreshToken });

        // Remove tokens from storage after logout
        await tokenManager.removeTokens();

        return response;
      } else {
        throw new Error("Refresh token not found");
      }
    } catch (error) {
      console.error("Error during logout:", error);
      throw error;
    }
  },
};

export default api;
