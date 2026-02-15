'use client';
import React from 'react';
import { useRouter } from 'next/navigation';
import { useSuppliers } from '@/hooks/useSuppliers';
import { SupplierList } from '@/components/suppliers/SupplierList';
import { Loader } from '@/components/ui/Loader';

export default function SuppliersPage() {
  const { suppliers, loading } = useSuppliers();
  const router = useRouter();

  if (loading) return <Loader />;

  return (
    <div>
      <h1 className='page-title'>Suppliers</h1>
      <SupplierList
        suppliers={suppliers}
        onSelect={(s) => router.push(`/dashboard/suppliers/${s.id}`)}
      />
    </div>
  );
}
