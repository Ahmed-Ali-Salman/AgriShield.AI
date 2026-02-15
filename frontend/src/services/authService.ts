import api from './api';
import { LoginInput, RegisterInput, TokenResponse } from '@/types/auth';

export const authService = {
    login: (data: LoginInput) => api.post<TokenResponse>('/auth/login', data),
    register: (data: RegisterInput) => api.post<TokenResponse>('/auth/register', data),
};
