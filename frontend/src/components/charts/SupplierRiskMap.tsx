'use client';
import React from 'react';
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Cell, ResponsiveContainer,
} from 'recharts';
import { getRiskColor } from '@/lib/formatters';

interface SupplierRiskMapProps {
  suppliers: Array<{ name: string; score: number; level: string }>;
}

export function SupplierRiskMap({ suppliers }: SupplierRiskMapProps) {
  if (!suppliers.length) {
    return (
      <div className='chart-empty'>
        <p>No scored suppliers.</p>
      </div>
    );
  }

  // Sort descending by score
  const sorted = [...suppliers].sort((a, b) => b.score - a.score);

  return (
    <div style={{ width: '100%', height: Math.max(260, sorted.length * 40) }}>
      <ResponsiveContainer>
        <BarChart
          data={sorted}
          layout='vertical'
          margin={{ top: 8, right: 24, left: 0, bottom: 0 }}
        >
          <CartesianGrid strokeDasharray='3 3' stroke='#2d3348' horizontal={false} />
          <XAxis
            type='number'
            domain={[0, 100]}
            stroke='#94a3b8'
            fontSize={12}
            tickLine={false}
          />
          <YAxis
            dataKey='name'
            type='category'
            width={120}
            stroke='#94a3b8'
            fontSize={12}
            tickLine={false}
          />
          <Tooltip
            contentStyle={{
              background: '#1a1d27',
              border: '1px solid #2d3348',
              borderRadius: 8,
              color: '#e2e8f0',
              fontSize: 13,
            }}
            formatter={(value: number) => [`${value.toFixed(1)}`, 'Risk Score']}
          />
          <Bar dataKey='score' radius={[0, 4, 4, 0]} barSize={20}>
            {sorted.map((entry, index) => (
              <Cell key={index} fill={getRiskColor(entry.level)} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
