import { useState } from 'react'
import { authService, LoginData, RegisterData } from '../services/auth-service'

export function useAuth() {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const login = async (data: LoginData) => {
    try {
      setLoading(true)
      setError(null)
      return await authService.login(data)
    } catch (err) {
      setError('Invalid email or password')
      throw err
    } finally {
      setLoading(false)
    }
  }

  const register = async (data: RegisterData) => {
    try {
      setLoading(true)
      setError(null)
      return await authService.register(data)
    } catch (err) {
      setError('Registration failed')
      throw err
    } finally {
      setLoading(false)
    }
  }

  const logout = async () => {
    try {
      setLoading(true)
      await authService.logout()
    } finally {
      setLoading(false)
    }
  }

  return {
    login,
    register,
    logout,
    loading,
    error
  }
}

