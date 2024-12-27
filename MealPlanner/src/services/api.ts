import axios from 'axios'
import * as SecureStore from 'expo-secure-store'
import type { AuthTokens, LoginCredentials, RegisterCredentials, User } from '../types/auth'

const api = axios.create({
  baseURL: 'https://api.yourbackend.com', // Replace with your API URL
})

// Request interceptor to add auth token
api.interceptors.request.use(async (config) => {
  const token = await SecureStore.getItemAsync('accessToken')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Response interceptor to handle token refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config

    if (error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true
      const refreshToken = await SecureStore.getItemAsync('refreshToken')
      
      try {
        const { data } = await api.post<AuthTokens>('/auth/refresh', { refreshToken })
        await SecureStore.setItemAsync('accessToken', data.accessToken)
        await SecureStore.setItemAsync('refreshToken', data.refreshToken)
        
        originalRequest.headers.Authorization = `Bearer ${data.accessToken}`
        return api(originalRequest)
      } catch (refreshError) {
        // Refresh token expired, user needs to login again
        await logout()
        throw refreshError
      }
    }
    
    return Promise.reject(error)
  }
)

export async function login(credentials: LoginCredentials) {
  const { data } = await api.post<AuthTokens & { user: User }>('/auth/login', credentials)
  await SecureStore.setItemAsync('accessToken', data.accessToken)
  await SecureStore.setItemAsync('refreshToken', data.refreshToken)
  return data
}

export async function register(credentials: RegisterCredentials) {
  const { data } = await api.post<AuthTokens & { user: User }>('/auth/register', credentials)
  await SecureStore.setItemAsync('accessToken', data.accessToken)
  await SecureStore.setItemAsync('refreshToken', data.refreshToken)
  return data
}

export async function logout() {
  await SecureStore.deleteItemAsync('accessToken')
  await SecureStore.deleteItemAsync('refreshToken')
}

export async function getCurrentUser() {
  const { data } = await api.get<User>('/auth/me')
  return data
}

