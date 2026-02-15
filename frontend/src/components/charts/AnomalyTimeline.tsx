'use client';
import React from 'react';

interface AnomalyTimelineProps {
  data: Array<{ date: string; count: number; }>;
}

export function AnomalyTimeline({ data }: AnomalyTimelineProps) {
  // Placeholder — will use Recharts in implementation
  return (
    <div className='anomaly-timeline'>
      <h4>Anomaly Timeline</h4>
      <p>Timeline chart placeholder — {data.length} data points</p>
    </div>
  );
}
