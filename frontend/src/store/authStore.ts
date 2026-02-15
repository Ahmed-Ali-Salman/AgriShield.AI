import { create } from 'zustand';

interface AuthState {
    token: string | null;
    role: string | null;
    setAuth: (token: string, role: string) => void;
    clearAuth: () => void;
}

export const useAuthStore = create<AuthState>((set) => ({
    token: typeof window !== 'undefined' ? localStorage.getItem('access_token') : null,
    role: null,
    setAuth: (token, role) => {
        localStorage.setItem('access_token', token);
        set({ token, role });
    },
    clearAuth: () => {
        localStorage.removeItem('access_token');
        set({ token: null, role: null });
    },
}));
