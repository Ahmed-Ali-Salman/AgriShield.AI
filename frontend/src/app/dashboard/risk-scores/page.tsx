'use client';
import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { Card } from '@/components/ui/Card';
import { Loader } from '@/components/ui/Loader';
import { Badge } from '@/components/ui/Badge';
import { supplierService } from '@/services/supplierService';
import { riskScoreService } from '@/services/riskScoreService';
import { Supplier } from '@/types/supplier';
import { RiskScore } from '@/types/riskScore';
import { formatScore, getRiskColor } from '@/lib/formatters';

interface SupplierWithScore extends Supplier {
  latestScore?: RiskScore;
}

export default function RiskScoresPage() {
  const [items, setItems] = useState<SupplierWithScore[]>([]);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    async function load() {
      try {
        const suppRes = await supplierService.list(0, 100);
        const suppliers = suppRes.data;

        // Fetch latest score for each supplier
        const enriched: SupplierWithScore[] = await Promise.all(
          suppliers.map(async (s) => {
            try {
              const histRes = await riskScoreService.getHistory(s.id, 1);
              return { ...s, latestScore: histRes.data[0] || undefined };
            } catch {
              return { ...s };
            }
          })
        );

        // Sort by score descending (unscored at bottom)
        enriched.sort((a, b) => {
          const sa = a.latestScore?.overall_score ?? -1;
          const sb = b.latestScore?.overall_score ?? -1;
          return sb - sa;
        });

        setItems(enriched);
      } catch (e) {
        console.error('Failed to load risk scores:', e);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  if (loading) return <Loader />;

  return (
    <div>
      <h1 className='page-title'>Risk Scores</h1>
      <Card>
        <table className='table'>
          <thead>
            <tr>
              <th>Supplier</th>
              <th>Country</th>
              <th>Score</th>
              <th>Risk Level</th>
              <th style={{ width: '150px' }}>Bar</th>
            </tr>
          </thead>
          <tbody>
            {items.map((item) => (
              <tr
                key={item.id}
                className='clickable'
                onClick={() => router.push(`/dashboard/suppliers/${item.id}`)}
              >
                <td><strong>{item.name}</strong></td>
                <td>{item.country}</td>
                <td>
                  {item.latestScore
                    ? formatScore(item.latestScore.overall_score)
                    : <span style={{ color: 'var(--color-text-muted)' }}>—</span>
                  }
                </td>
                <td>
                  {item.latestScore
                    ? <Badge level={item.latestScore.risk_level} />
                    : <span style={{ color: 'var(--color-text-muted)' }}>Not scored</span>
                  }
                </td>
                <td>
                  {item.latestScore && (
                    <div className='risk-score-bar'>
                      <div
                        className='risk-score-bar-fill'
                        style={{
                          width: `${item.latestScore.overall_score}%`,
                          backgroundColor: getRiskColor(item.latestScore.risk_level),
                        }}
                      />
                    </div>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        {items.length === 0 && (
          <p style={{ padding: 16, color: 'var(--color-text-muted)', textAlign: 'center' }}>
            No suppliers found.
          </p>
        )}
      </Card>
    </div>
  );
}
