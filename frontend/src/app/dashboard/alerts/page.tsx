'use client';
import React, { useState, useEffect, useCallback } from 'react';
import { Card } from '@/components/ui/Card';
import { Loader } from '@/components/ui/Loader';
import { Badge } from '@/components/ui/Badge';
import { Button } from '@/components/ui/Button';
import { alertService } from '@/services/alertService';
import { formatDate } from '@/lib/formatters';
import { Alert } from '@/types/alert';

const TABS = [
  { key: undefined as string | undefined, label: 'All' },
  { key: 'open', label: 'Open' },
  { key: 'acknowledged', label: 'Acknowledged' },
  { key: 'resolved', label: 'Resolved' },
];

export default function AlertsPage() {
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState<string | undefined>(undefined);

  const loadAlerts = useCallback(async () => {
    setLoading(true);
    try {
      const res = await alertService.list(filter);
      setAlerts(res.data);
    } catch (e) {
      console.error('Failed to load alerts', e);
    } finally {
      setLoading(false);
    }
  }, [filter]);

  useEffect(() => { loadAlerts(); }, [loadAlerts]);

  const handleStatusChange = async (id: string, status: 'acknowledged' | 'resolved') => {
    try {
      await alertService.updateStatus(id, status);
      loadAlerts();
    } catch (e) {
      console.error('Failed to update alert:', e);
    }
  };

  return (
    <div>
      <h1 className='page-title'>Alerts</h1>

      {/* Tabs */}
      <div className='tab-bar'>
        {TABS.map((tab) => (
          <button
            key={tab.label}
            className={`tab ${filter === tab.key ? 'tab-active' : ''}`}
            onClick={() => setFilter(tab.key)}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {loading ? (
        <Loader />
      ) : alerts.length === 0 ? (
        <Card>
          <p style={{ color: 'var(--color-text-muted)', textAlign: 'center', padding: 24 }}>
            No {filter || ''} alerts found.
          </p>
        </Card>
      ) : (
        <div className='alert-list'>
          {alerts.map(alert => (
            <Card key={alert.id}>
              <div className='alert-card-header'>
                <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
                  <strong>{alert.title}</strong>
                  <Badge level={alert.severity} />
                </div>
                <Badge level={alert.status === 'open' ? 'warning' : alert.status === 'resolved' ? 'low' : 'medium'} />
              </div>
              <p style={{ fontSize: '0.9rem', color: 'var(--color-text-muted)', marginBottom: 12 }}>
                {alert.description}
              </p>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <small style={{ color: 'var(--color-text-muted)' }}>
                  Triggered: {formatDate(alert.triggered_at)}
                  {alert.resolved_at && ` · Resolved: ${formatDate(alert.resolved_at)}`}
                </small>
                {alert.status === 'open' && (
                  <div style={{ display: 'flex', gap: 8 }}>
                    <Button variant='secondary' onClick={() => handleStatusChange(alert.id, 'acknowledged')} style={{ fontSize: '0.8rem', padding: '4px 12px' }}>
                      Acknowledge
                    </Button>
                    <Button variant='primary' onClick={() => handleStatusChange(alert.id, 'resolved')} style={{ fontSize: '0.8rem', padding: '4px 12px' }}>
                      Resolve
                    </Button>
                  </div>
                )}
                {alert.status === 'acknowledged' && (
                  <Button variant='primary' onClick={() => handleStatusChange(alert.id, 'resolved')} style={{ fontSize: '0.8rem', padding: '4px 12px' }}>
                    Resolve
                  </Button>
                )}
              </div>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
