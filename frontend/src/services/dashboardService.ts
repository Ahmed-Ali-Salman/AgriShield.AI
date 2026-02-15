import api from './api';

export interface DashboardSummary {
    total_suppliers: number;
    open_alerts: number;
    high_risk_count: number;
    avg_risk_score: number;
}

export const dashboardService = {
    getSummary: () => api.get<DashboardSummary>('/dashboard/summary'),
};
