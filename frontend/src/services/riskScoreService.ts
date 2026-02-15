import api from './api';
import { RiskScore, RiskScoreInput } from '@/types/riskScore';

export const riskScoreService = {
    calculate: (supplierId: string, data: RiskScoreInput) =>
        api.post<RiskScore>(`/risk-scores/${supplierId}`, data),
    getHistory: (supplierId: string, limit = 30) =>
        api.get<RiskScore[]>(`/risk-scores/${supplierId}/history`, { params: { limit } }),
};
