'use client';
import React from 'react';
import { useAlerts } from '@/hooks/useAlerts';
import { Card } from '@/components/ui/Card';
import { Loader } from '@/components/ui/Loader';
import { Badge } from '@/components/ui/Badge';

export default function AlertsPage() {
  const { alerts, loading } = useAlerts();
  if (loading) return <Loader />;
  return (
    <div>
      <h1 className='page-title'>Alerts</h1>
      {alerts.map(alert => (
        <Card key={alert.id} title={alert.title}>
          <Badge level={alert.severity} />
          <p>{alert.description}</p>
        </Card>
      ))}
      {!alerts.length && <p>No alerts.</p>}
    </div>
  );
}
