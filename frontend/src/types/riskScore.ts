export interface RiskScore {
    id: string;
    supplier_id: string;
    overall_score: number;
    risk_level: 'low' | 'medium' | 'high' | 'critical';
    computed_at: string;
    notes: string;
}

export interface RiskScoreInput {
    it_security_posture: number;
    data_consistency: number;
    delivery_reliability: number;
    compliance_audit: number;
    external_risk_factors: number;
}
