import api from './api';
import { Alert } from '@/types/alert';

export const alertService = {
    list: (status?: string) =>
        api.get<Alert[]>('/alerts', { params: { status } }),
    create: (data: { supplier_id: string; title: string; description: string; severity: string }) =>
        api.post<Alert>('/alerts', data),
    updateStatus: (id: string, status: 'acknowledged' | 'resolved') =>
        api.patch<Alert>(`/alerts/${id}`, { status }),
};
