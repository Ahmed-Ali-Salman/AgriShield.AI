import React from 'react';
import { Badge } from '@/components/ui/Badge';

interface RiskBadgeProps { level: string; score: number; }

export function RiskBadge({ level, score }: RiskBadgeProps) {
  return (
    <div className='risk-badge'>
      <Badge level={level} />
      <span className='risk-score-value'>{score.toFixed(1)}</span>
    </div>
  );
}
