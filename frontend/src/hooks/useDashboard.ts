'use client';
import { useState, useEffect } from 'react';
import { dashboardService, DashboardSummary } from '@/services/dashboardService';

export function useDashboard() {
    const [data, setData] = useState<DashboardSummary | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        dashboardService
            .getSummary()
            .then((res) => setData(res.data))
            .catch(console.error)
            .finally(() => setLoading(false));
    }, []);

    return { data, loading };
}
