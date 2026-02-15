import React from 'react';
import { getRiskColor, getRiskLabel } from '@/lib/formatters';

interface BadgeProps { level: string; }

export function Badge({ level }: BadgeProps) {
  return <span className='badge' style={{ backgroundColor: getRiskColor(level) }}>{getRiskLabel(level)}</span>;
}
