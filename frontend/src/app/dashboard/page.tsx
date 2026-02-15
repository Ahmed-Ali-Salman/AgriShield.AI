'use client';
import React from 'react';
import { Card } from '@/components/ui/Card';
import { Loader } from '@/components/ui/Loader';
import { useDashboard } from '@/hooks/useDashboard';

export default function DashboardPage() {
  const { data, loading } = useDashboard();

  if (loading) return <Loader />;

  return (
    <div>
      <h1 className='page-title'>Dashboard</h1>
      <div className='stats-grid'>
        <Card className='stat-card'>
          <div className='stat-value'>{data?.total_suppliers ?? '--'}</div>
          <div className='stat-label'>Total Suppliers</div>
        </Card>
        <Card className='stat-card'>
          <div className='stat-value'>{data?.open_alerts ?? '--'}</div>
          <div className='stat-label'>Open Alerts</div>
        </Card>
        <Card className='stat-card'>
          <div className='stat-value'>--</div>
          <div className='stat-label'>High Risk Suppliers</div>
        </Card>
        <Card className='stat-card'>
          <div className='stat-value'>--</div>
          <div className='stat-label'>Avg Risk Score</div>
        </Card>
      </div>
    </div>
  );
}
