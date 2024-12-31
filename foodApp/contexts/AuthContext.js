import React, { createContext, useContext, useState, useEffect } from "react";
import { tokenManager } from "../utils/tokenManager";
import api from "../utils/api";

const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    checkAuth();
  }, []);

  const checkAuth = async () => {
    try {
      const accessToken = await tokenManager.getAccessToken();
      if (accessToken) {
        setIsAuthenticated(true);
      }
    } catch (error) {
      console.error("Error checking authentication:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const login = async (tokens) => {
    await tokenManager.setTokens(tokens);
    setIsAuthenticated(true);
  };

  const logout = async () => {
    try {
      const refreshToken = await tokenManager.getRefreshToken();
      if (refreshToken) {
        await api.post("/logout/", { refresh: refreshToken });
      }
    } catch (error) {
      console.error("Error during logout:", error);
    } finally {
      await tokenManager.removeTokens();
      setIsAuthenticated(false);
    }
  };

  return (
    <AuthContext.Provider value={{ isAuthenticated, isLoading, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}
