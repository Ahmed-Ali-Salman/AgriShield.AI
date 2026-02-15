export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

export const RISK_LEVELS = {
    LOW: 'low',
    MEDIUM: 'medium',
    HIGH: 'high',
    CRITICAL: 'critical',
} as const;

export const ALERT_SEVERITIES = {
    INFO: 'info',
    WARNING: 'warning',
    CRITICAL: 'critical',
} as const;

export const SUPPLIER_CATEGORIES = [
    'grain',
    'dairy',
    'meat',
    'produce',
    'logistics',
    'packaging',
    'processing',
] as const;
