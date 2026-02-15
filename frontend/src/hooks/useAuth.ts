'use client';
import { useState } from 'react';
import { authService } from '@/services/authService';
import { LoginInput, TokenResponse } from '@/types/auth';

export function useAuth() {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const login = async (data: LoginInput): Promise<TokenResponse | undefined> => {
        setLoading(true);
        setError(null);
        try {
            const res = await authService.login(data);
            // Store in localStorage for API interceptor
            localStorage.setItem('access_token', res.data.access_token);
            // Store in cookie for Next.js middleware auth guard
            document.cookie = `auth_token=${res.data.access_token}; path=/; max-age=${60 * 60 * 24 * 7}; SameSite=Lax`;
            return res.data;
        } catch (e: any) {
            setError(e.response?.data?.detail || 'Login failed');
        } finally {
            setLoading(false);
        }
    };

    const logout = () => {
        localStorage.removeItem('access_token');
        document.cookie = 'auth_token=; path=/; max-age=0';
        window.location.href = '/login';
    };

    return { login, logout, loading, error };
}
