'use client';
import React from 'react';
import { getRiskColor } from '@/lib/formatters';

interface RiskScoreGaugeProps { score: number; level: string; }

export function RiskScoreGauge({ score, level }: RiskScoreGaugeProps) {
  const color = getRiskColor(level);
  const dashArray = `${(score / 100) * 314} 314`;
  return (
    <div className='gauge'>
      <svg viewBox='0 0 120 120' width='120' height='120'>
        <circle cx='60' cy='60' r='50' fill='none' stroke='var(--color-border)' strokeWidth='10' />
        <circle cx='60' cy='60' r='50' fill='none' stroke={color} strokeWidth='10'
          strokeDasharray={dashArray} strokeLinecap='round'
          transform='rotate(-90 60 60)' style={{ transition: 'stroke-dasharray 0.6s ease' }} />
        <text x='60' y='65' textAnchor='middle' fontSize='20' fontWeight='bold' fill={color}>
          {score.toFixed(0)}
        </text>
      </svg>
      <p className='gauge-label'>{level.toUpperCase()}</p>
    </div>
  );
}
