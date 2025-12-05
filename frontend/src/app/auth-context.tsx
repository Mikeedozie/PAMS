"use client";
import React, { createContext, useContext, useEffect, useState, ReactNode, useCallback } from 'react';

interface User {
  id: number;
  username: string;
  email: string;
  role?: string;
  full_name?: string;
}

interface AuthContextType {
  user: User | null;
  token: string | null;
  loading: boolean;
  login: (username: string, password: string) => Promise<boolean>;
  register: (data: { username: string; email: string; password: string; full_name?: string }) => Promise<boolean>;
  logout: () => void;
  refreshProfile: () => Promise<void>;
  tokenIssuedAt?: number;
  tokenAgeSeconds?: () => number;
  authError?: string | null;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

const STORAGE_KEY = 'pams_auth_token';

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [authError, setAuthError] = useState<string | null>(null);
  const [tokenIssuedAt, setTokenIssuedAt] = useState<number | undefined>(undefined);

  const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

  useEffect(() => {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (stored) {
      setToken(stored);
      // fetch profile
      fetchProfile(stored);
    } else {
      setLoading(false);
    }
  }, []);

  const fetchProfile = async (t: string) => {
    try {
      const controller = new AbortController();
      const id = setTimeout(() => controller.abort(), 8000);
      const res = await fetch(`${apiUrl}/api/auth/me`, {
        headers: { Authorization: `Bearer ${t}` },
        signal: controller.signal,
      });
      clearTimeout(id);
      if (res.ok) {
        const data = await res.json();
        setUser(data);
      } else {
        localStorage.removeItem(STORAGE_KEY);
        setToken(null);
        setUser(null);
      }
    } catch (e:any) {
      console.error('Profile fetch failed', e);
      setAuthError(e.name === 'AbortError' ? 'Profile request timed out' : 'Profile load failed');
    } finally {
      setLoading(false);
    }
  };

  const login = useCallback(async (username: string, password: string) => {
    setAuthError(null);
    try {
      const body = new URLSearchParams();
      body.append('username', username);
      body.append('password', password);
      body.append('grant_type', 'password');
      const controller = new AbortController();
      const id = setTimeout(() => controller.abort(), 8000);
      const res = await fetch(`${apiUrl}/api/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body,
        signal: controller.signal,
      });
      clearTimeout(id);
      if (!res.ok) {
        setAuthError(res.status === 401 ? 'Invalid credentials' : `Login failed (${res.status})`);
        return false;
      }
      const data = await res.json();
      localStorage.setItem(STORAGE_KEY, data.access_token);
      setToken(data.access_token);
      setTokenIssuedAt(Date.now());
      await fetchProfile(data.access_token);
      return true;
    } catch (e:any) {
      setAuthError(e.name === 'AbortError' ? 'Login timed out' : 'Network error');
      console.error('Login failed', e);
      return false;
    }
  }, [apiUrl]);

  const register = useCallback(async (payload: { username: string; email: string; password: string; full_name?: string }) => {
    setAuthError(null);
    try {
      const res = await fetch(`${apiUrl}/api/auth/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      if (!res.ok) {
        setAuthError('Registration failed');
        return false;
      }
      return await login(payload.username, payload.password);
    } catch (e:any) {
      setAuthError('Network error');
      console.error('Register failed', e);
      return false;
    }
  }, [apiUrl, login]);

  const logout = () => {
    localStorage.removeItem(STORAGE_KEY);
    setToken(null);
    setUser(null);
    if (typeof window !== 'undefined') {
      window.location.href = '/landing';
    }
  };

  const refreshProfile = async () => {
    if (token) await fetchProfile(token);
  };

  const tokenAgeSeconds = useCallback(() => tokenIssuedAt ? Math.floor((Date.now() - tokenIssuedAt)/1000) : undefined, [tokenIssuedAt]);

  return (
    <AuthContext.Provider value={{ user, token, loading, login, register, logout, refreshProfile, tokenIssuedAt, tokenAgeSeconds, authError }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth must be used within AuthProvider');
  return ctx;
}
