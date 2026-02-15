export function formatDate(dateStr: string): string {
    return new Date(dateStr).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
    });
}

export function formatScore(score: number): string {
    return score.toFixed(1);
}

export function getRiskColor(level: string): string {
    const colors: Record<string, string> = {
        low: '#22c55e',
        medium: '#f59e0b',
        high: '#ef4444',
        critical: '#dc2626',
    };
    return colors[level] || '#6b7280';
}

export function getRiskLabel(level: string): string {
    return level.charAt(0).toUpperCase() + level.slice(1);
}
