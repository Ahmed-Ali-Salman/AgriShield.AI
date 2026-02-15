export interface Alert {
    id: string;
    supplier_id: string;
    title: string;
    description: string;
    severity: 'info' | 'warning' | 'critical';
    status: 'open' | 'acknowledged' | 'resolved';
    triggered_at: string;
    resolved_at: string | null;
}
