import { createContext, useCallback, useContext, useEffect, useMemo, useState } from 'react';
import { api } from '../api/client';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [email, setEmail] = useState(api.getEmail());
  const [basketCount, setBasketCount] = useState(0);
  const isAuthenticated = Boolean(email && api.getToken());

  const refreshBasket = useCallback(async () => {
    try {
      const basket = await api.getBasket();
      setBasketCount(basket.item_count);
    } catch {
      setBasketCount(0);
    }
  }, []);

  useEffect(() => {
    refreshBasket();
  }, [refreshBasket, email]);

  const login = useCallback(async (loginEmail, password) => {
    const result = await api.login(loginEmail, password);
    api.setAuth(result.access_token, result.email);
    setEmail(result.email);
    await refreshBasket();
    return result;
  }, [refreshBasket]);

  const register = useCallback(async (registerEmail, password) => {
    const result = await api.register(registerEmail, password);
    api.setAuth(result.access_token, result.email);
    setEmail(result.email);
    await refreshBasket();
    return result;
  }, [refreshBasket]);

  const logout = useCallback(() => {
    api.clearAuth();
    setEmail(null);
    setBasketCount(0);
  }, []);

  const value = useMemo(
    () => ({
      email,
      isAuthenticated,
      basketCount,
      refreshBasket,
      login,
      register,
      logout,
    }),
    [email, isAuthenticated, basketCount, refreshBasket, login, register, logout],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
}
