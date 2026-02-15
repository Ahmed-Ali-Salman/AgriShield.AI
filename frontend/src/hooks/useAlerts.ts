'use client';
import { useState, useEffect } from 'react';
import { alertService } from '@/services/alertService';
import { Alert } from '@/types/alert';

export function useAlerts(status?: string) {
    const [alerts, setAlerts] = useState<Alert[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        alertService.list(status)
            .then(res => setAlerts(res.data))
            .catch(console.error)
            .finally(() => setLoading(false));
    }, [status]);

    return { alerts, loading };
}
