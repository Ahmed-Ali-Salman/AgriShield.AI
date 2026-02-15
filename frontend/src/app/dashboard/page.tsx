'use client';
import React, { useState, useEffect } from 'react';
import { Card } from '@/components/ui/Card';
import { Loader } from '@/components/ui/Loader';
import { useDashboard } from '@/hooks/useDashboard';
import { useAlerts } from '@/hooks/useAlerts';
import { Badge } from '@/components/ui/Badge';
import { SupplierRiskMap } from '@/components/charts/SupplierRiskMap';
import { supplierService } from '@/services/supplierService';
import { riskScoreService } from '@/services/riskScoreService';
import { formatDate } from '@/lib/formatters';

export default function DashboardPage() {
  const { data, loading } = useDashboard();
  const { alerts, loading: alertsLoading } = useAlerts();
  const [riskMapData, setRiskMapData] = useState<Array<{ name: string; score: number; level: string }>>([]);

  useEffect(() => {
    async function loadRiskMap() {
      try {
        const suppRes = await supplierService.list(0, 100);
        const items = await Promise.all(
          suppRes.data.map(async (s) => {
            try {
              const histRes = await riskScoreService.getHistory(s.id, 1);
              const latest = histRes.data[0];
              return latest ? { name: s.name, score: latest.overall_score, level: latest.risk_level } : null;
            } catch { return null; }
          })
        );
        setRiskMapData(items.filter(Boolean) as Array<{ name: string; score: number; level: string }>);
      } catch { /* ignore */ }
    }
    loadRiskMap();
  }, []);

  if (loading) return <Loader />;

  return (
    <div>
      <h1 className='page-title'>Dashboard</h1>

      {/* --- Stats Grid --- */}
      <div className='stats-grid'>
        <Card className='stat-card'>
          <div className='stat-value'>{data?.total_suppliers ?? '--'}</div>
          <div className='stat-label'>Total Suppliers</div>
        </Card>
        <Card className='stat-card'>
          <div className='stat-value' style={{ color: (data?.open_alerts ?? 0) > 0 ? 'var(--color-warning)' : undefined }}>
            {data?.open_alerts ?? '--'}
          </div>
          <div className='stat-label'>Open Alerts</div>
        </Card>
        <Card className='stat-card'>
          <div className='stat-value' style={{ color: (data?.high_risk_count ?? 0) > 0 ? 'var(--color-danger)' : undefined }}>
            {data?.high_risk_count ?? '--'}
          </div>
          <div className='stat-label'>High Risk Suppliers</div>
        </Card>
        <Card className='stat-card'>
          <div className='stat-value'>{data?.avg_risk_score?.toFixed(1) ?? '--'}</div>
          <div className='stat-label'>Avg Risk Score</div>
        </Card>
      </div>

      {/* --- Charts Row --- */}
      <div className='detail-grid'>
        <Card title='Supplier Risk Overview'>
          <SupplierRiskMap suppliers={riskMapData} />
        </Card>
        <Card title='Recent Alerts'>
          {alertsLoading ? (
            <Loader />
          ) : alerts.length === 0 ? (
            <p style={{ color: 'var(--color-text-muted)' }}>No alerts yet.</p>
          ) : (
            <div className='alert-list'>
              {alerts.slice(0, 5).map(alert => (
                <div key={alert.id} className='card' style={{ padding: '12px 16px' }}>
                  <div className='alert-card-header'>
                    <strong>{alert.title}</strong>
                    <Badge level={alert.severity} />
                  </div>
                  <p style={{ fontSize: '0.85rem', color: 'var(--color-text-muted)' }}>{alert.description}</p>
                  <small style={{ color: 'var(--color-text-muted)' }}>{formatDate(alert.triggered_at)}</small>
                </div>
              ))}
            </div>
          )}
        </Card>
      </div>
    </div>
  );
}
