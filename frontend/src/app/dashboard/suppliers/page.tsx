'use client';
import React from 'react';
import { useSuppliers } from '@/hooks/useSuppliers';
import { SupplierList } from '@/components/suppliers/SupplierList';
import { Loader } from '@/components/ui/Loader';

export default function SuppliersPage() {
  const { suppliers, loading } = useSuppliers();
  if (loading) return <Loader />;
  return (
    <div>
      <h1 className='page-title'>Suppliers</h1>
      <SupplierList suppliers={suppliers} />
    </div>
  );
}
