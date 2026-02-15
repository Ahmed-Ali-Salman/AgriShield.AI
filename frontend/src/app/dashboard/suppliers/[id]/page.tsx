'use client';
import React, { useState, useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { Card } from '@/components/ui/Card';
import { Loader } from '@/components/ui/Loader';
import { Badge } from '@/components/ui/Badge';
import { RiskScoreGauge } from '@/components/charts/RiskScoreGauge';
import { Button } from '@/components/ui/Button';
import { supplierService } from '@/services/supplierService';
import { riskScoreService } from '@/services/riskScoreService';
import { alertService } from '@/services/alertService';
import { formatDate, formatScore } from '@/lib/formatters';
import { Supplier } from '@/types/supplier';
import { RiskScore } from '@/types/riskScore';
import { Alert } from '@/types/alert';

export default function SupplierDetailPage() {
    const { id } = useParams<{ id: string }>();
    const router = useRouter();
    const [supplier, setSupplier] = useState<Supplier | null>(null);
    const [scores, setScores] = useState<RiskScore[]>([]);
    const [alerts, setAlerts] = useState<Alert[]>([]);
    const [loading, setLoading] = useState(true);
    const [calculating, setCalculating] = useState(false);

    useEffect(() => {
        if (!id) return;
        Promise.all([
            supplierService.getById(id).then(r => setSupplier(r.data)),
            riskScoreService.getHistory(id).then(r => setScores(r.data)),
            alertService.list().then(r => setAlerts(r.data.filter(a => a.supplier_id === id))),
        ])
            .catch(console.error)
            .finally(() => setLoading(false));
    }, [id]);

    const handleCalculateRisk = async () => {
        if (!id) return;
        setCalculating(true);
        try {
            const res = await riskScoreService.calculate(id, {
                it_security_posture: Math.round(Math.random() * 40 + 30),
                data_consistency: Math.round(Math.random() * 40 + 40),
                delivery_reliability: Math.round(Math.random() * 50 + 30),
                compliance_audit: Math.round(Math.random() * 40 + 40),
                external_risk_factors: Math.round(Math.random() * 60 + 10),
            });
            setScores(prev => [res.data, ...prev]);
        } catch (e) {
            console.error('Risk calculation failed:', e);
        } finally {
            setCalculating(false);
        }
    };

    if (loading) return <Loader />;
    if (!supplier) return <p>Supplier not found.</p>;

    const latestScore = scores[0];

    return (
        <div>
            <button onClick={() => router.back()} className='btn btn-secondary' style={{ marginBottom: 16 }}>
                &larr; Back
            </button>
            <h1 className='page-title'>{supplier.name}</h1>

            {/* Supplier Info */}
            <div className='detail-meta'>
                <div className='detail-meta-item'>
                    <span className='detail-meta-label'>Country</span>
                    <span className='detail-meta-value'>{supplier.country}</span>
                </div>
                <div className='detail-meta-item'>
                    <span className='detail-meta-label'>Category</span>
                    <span className='detail-meta-value'>{supplier.category}</span>
                </div>
                <div className='detail-meta-item'>
                    <span className='detail-meta-label'>Status</span>
                    <span className='detail-meta-value'>{supplier.is_active ? '✅ Active' : '⛔ Inactive'}</span>
                </div>
                <div className='detail-meta-item'>
                    <span className='detail-meta-label'>Added</span>
                    <span className='detail-meta-value'>{formatDate(supplier.created_at)}</span>
                </div>
            </div>

            {/* Risk Score + Actions */}
            <div className='detail-grid'>
                <Card title='Risk Score'>
                    {latestScore ? (
                        <div style={{ display: 'flex', alignItems: 'center', gap: 24 }}>
                            <RiskScoreGauge score={latestScore.overall_score} level={latestScore.risk_level} />
                            <div>
                                <p><strong>Score:</strong> {formatScore(latestScore.overall_score)}</p>
                                <p><strong>Level:</strong> <Badge level={latestScore.risk_level} /></p>
                                <p style={{ fontSize: '0.8rem', color: 'var(--color-text-muted)', marginTop: 8 }}>
                                    Computed: {formatDate(latestScore.computed_at)}
                                </p>
                            </div>
                        </div>
                    ) : (
                        <p style={{ color: 'var(--color-text-muted)' }}>No risk score computed yet.</p>
                    )}
                    <Button onClick={handleCalculateRisk} loading={calculating} variant='primary' style={{ marginTop: 16 }}>
                        {latestScore ? 'Recalculate Risk' : 'Calculate Risk Score'}
                    </Button>
                </Card>

                <Card title={`Alerts (${alerts.length})`}>
                    {alerts.length === 0 ? (
                        <p style={{ color: 'var(--color-text-muted)' }}>No alerts for this supplier.</p>
                    ) : (
                        <div className='alert-list'>
                            {alerts.slice(0, 5).map(alert => (
                                <div key={alert.id} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '8px 0', borderBottom: '1px solid var(--color-border)' }}>
                                    <span>{alert.title}</span>
                                    <Badge level={alert.severity} />
                                </div>
                            ))}
                        </div>
                    )}
                </Card>
            </div>

            {/* Score History */}
            {scores.length > 0 && (
                <Card title='Score History'>
                    <table className='table'>
                        <thead>
                            <tr>
                                <th>Date</th>
                                <th>Score</th>
                                <th>Level</th>
                                <th>Notes</th>
                            </tr>
                        </thead>
                        <tbody>
                            {scores.map(s => (
                                <tr key={s.id}>
                                    <td>{formatDate(s.computed_at)}</td>
                                    <td>{formatScore(s.overall_score)}</td>
                                    <td><Badge level={s.risk_level} /></td>
                                    <td style={{ fontSize: '0.85rem', color: 'var(--color-text-muted)' }}>{s.notes || '—'}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </Card>
            )}
        </div>
    );
}
