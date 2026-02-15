'use client';
import React from 'react';

interface SupplierRiskMapProps {
  suppliers: Array<{ name: string; score: number; level: string; }>;
}

export function SupplierRiskMap({ suppliers }: SupplierRiskMapProps) {
  // Placeholder — will use a heat map or treemap visualization
  return (
    <div className='risk-map'>
      <h4>Supplier Risk Map</h4>
      <p>Risk map placeholder — {suppliers.length} suppliers</p>
    </div>
  );
}
