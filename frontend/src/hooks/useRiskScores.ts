'use client';
import { useState, useEffect } from 'react';
import { riskScoreService } from '@/services/riskScoreService';
import { RiskScore } from '@/types/riskScore';

export function useRiskScores(supplierId: string) {
    const [scores, setScores] = useState<RiskScore[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        if (!supplierId) return;
        riskScoreService.getHistory(supplierId)
            .then(res => setScores(res.data))
            .catch(console.error)
            .finally(() => setLoading(false));
    }, [supplierId]);

    return { scores, loading };
}
