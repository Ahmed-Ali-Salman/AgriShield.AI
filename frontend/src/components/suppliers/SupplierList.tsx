import React from 'react';
import { Supplier } from '@/types/supplier';
import { SupplierCard } from './SupplierCard';

interface SupplierListProps { suppliers: Supplier[]; onSelect?: (s: Supplier) => void; }

export function SupplierList({ suppliers, onSelect }: SupplierListProps) {
  if (!suppliers.length) return <p>No suppliers found.</p>;
  return (
    <div className='supplier-list'>
      {suppliers.map(s => <SupplierCard key={s.id} supplier={s} onClick={() => onSelect?.(s)} />)}
    </div>
  );
}
