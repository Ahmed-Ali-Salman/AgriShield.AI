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
            localStorage.setItem('access_token', res.data.access_token);
            return res.data;
        } catch (e: any) {
            setError(e.response?.data?.detail || 'Login failed');
        } finally {
            setLoading(false);
        }
    };

    const logout = () => {
        localStorage.removeItem('access_token');
    };

    return { login, logout, loading, error };
}
