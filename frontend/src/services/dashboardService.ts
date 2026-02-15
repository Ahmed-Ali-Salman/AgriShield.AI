import api from './api';

export interface DashboardSummary {
    total_suppliers: number;
    open_alerts: number;
}

export const dashboardService = {
    getSummary: () => api.get<DashboardSummary>('/dashboard/summary'),
};
