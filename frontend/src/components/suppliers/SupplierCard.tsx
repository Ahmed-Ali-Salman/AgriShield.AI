import React from 'react';
import { Supplier } from '@/types/supplier';
import { Card } from '@/components/ui/Card';

interface SupplierCardProps { supplier: Supplier; onClick?: () => void; }

export function SupplierCard({ supplier, onClick }: SupplierCardProps) {
  return (
    <Card className='supplier-card' title={supplier.name}>
      <p><strong>Country:</strong> {supplier.country}</p>
      <p><strong>Category:</strong> {supplier.category}</p>
      <p><strong>Active:</strong> {supplier.is_active ? 'Yes' : 'No'}</p>
      {onClick && <button onClick={onClick} className='btn btn-secondary'>View Details</button>}
    </Card>
  );
}
