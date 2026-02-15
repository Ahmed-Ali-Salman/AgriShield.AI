'use client';
import React from 'react';
import {
    LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ReferenceLine,
} from 'recharts';
import { RiskScore } from '@/types/riskScore';
import { getRiskColor } from '@/lib/formatters';

interface RiskScoreTrendProps {
    scores: RiskScore[];
}

export function RiskScoreTrend({ scores }: RiskScoreTrendProps) {
    if (scores.length < 2) {
        return (
            <div className='chart-empty'>
                <p>At least 2 scores needed to show a trend.</p>
            </div>
        );
    }

    // Reverse so chart goes chronologically left-to-right
    const data = [...scores].reverse().map((s) => ({
        date: new Date(s.computed_at).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
        score: s.overall_score,
        level: s.risk_level,
    }));

    return (
        <div style={{ width: '100%', height: 260 }}>
            <ResponsiveContainer>
                <LineChart data={data} margin={{ top: 8, right: 16, left: 0, bottom: 0 }}>
                    <CartesianGrid strokeDasharray='3 3' stroke='#2d3348' />
                    <XAxis dataKey='date' stroke='#94a3b8' fontSize={12} tickLine={false} />
                    <YAxis domain={[0, 100]} stroke='#94a3b8' fontSize={12} tickLine={false} />
                    {/* Risk threshold lines */}
                    <ReferenceLine y={70} stroke='#ef4444' strokeDasharray='4 4' label={{ value: 'High', fill: '#ef4444', fontSize: 11 }} />
                    <ReferenceLine y={40} stroke='#f59e0b' strokeDasharray='4 4' label={{ value: 'Medium', fill: '#f59e0b', fontSize: 11 }} />
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
                    <Line
                        type='monotone'
                        dataKey='score'
                        stroke='#0f766e'
                        strokeWidth={2}
                        dot={{ r: 4, fill: '#0f766e', strokeWidth: 0 }}
                        activeDot={{ r: 6, fill: '#0f766e' }}
                    />
                </LineChart>
            </ResponsiveContainer>
        </div>
    );
}
