import axios from 'axios'
import { tokenManager } from './tokenManager'

const api = axios.create({
  baseURL: 'YOUR_API_URL',
  headers: {
    'Content-Type': 'application/json'
  }
})

// Add token to requests if it exists
api.interceptors.request.use(async (config) => {
  const token = await tokenManager.getToken()
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export const authAPI = {
  login: (credentials) => api.post('/login', credentials),
  register: (userData) => api.post('/register', userData),
  logout: () => api.post('/logout')
}

export default api

