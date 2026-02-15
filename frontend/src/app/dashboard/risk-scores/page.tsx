'use client';
import React from 'react';
import { Card } from '@/components/ui/Card';

export default function RiskScoresPage() {
  return (
    <div>
      <h1 className='page-title'>Risk Scores</h1>
      <Card title='Risk Score Overview'>
        <p>Supplier risk score rankings and trends.</p>
      </Card>
    </div>
  );
}
