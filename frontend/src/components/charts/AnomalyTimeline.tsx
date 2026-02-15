'use client';
import React from 'react';
import {
  AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
} from 'recharts';

interface AnomalyTimelineProps {
  data: Array<{ date: string; count: number }>;
}

export function AnomalyTimeline({ data }: AnomalyTimelineProps) {
  if (!data.length) {
    return (
      <div className='chart-empty'>
        <p>No anomaly data available.</p>
      </div>
    );
  }

  return (
    <div style={{ width: '100%', height: 260 }}>
      <ResponsiveContainer>
        <AreaChart data={data} margin={{ top: 8, right: 16, left: 0, bottom: 0 }}>
          <defs>
            <linearGradient id='anomalyGradient' x1='0' y1='0' x2='0' y2='1'>
              <stop offset='5%' stopColor='#ef4444' stopOpacity={0.3} />
              <stop offset='95%' stopColor='#ef4444' stopOpacity={0} />
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray='3 3' stroke='#2d3348' />
          <XAxis
            dataKey='date'
            stroke='#94a3b8'
            fontSize={12}
            tickLine={false}
          />
          <YAxis
            stroke='#94a3b8'
            fontSize={12}
            tickLine={false}
            allowDecimals={false}
          />
          <Tooltip
            contentStyle={{
              background: '#1a1d27',
              border: '1px solid #2d3348',
              borderRadius: 8,
              color: '#e2e8f0',
              fontSize: 13,
            }}
          />
          <Area
            type='monotone'
            dataKey='count'
            stroke='#ef4444'
            strokeWidth={2}
            fill='url(#anomalyGradient)'
            name='Anomalies'
          />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
}
