'use client';
import { useState, useEffect } from 'react';
import { supplierService } from '@/services/supplierService';
import { Supplier } from '@/types/supplier';

export function useSuppliers() {
    const [suppliers, setSuppliers] = useState<Supplier[]>([]);
    const [loading, setLoading] = useState(true);

    const fetchSuppliers = async () => {
        setLoading(true);
        try {
            const res = await supplierService.list();
            setSuppliers(res.data);
        } catch (e) {
            console.error('Failed to fetch suppliers:', e);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchSuppliers();
    }, []);

    return { suppliers, loading, refetch: fetchSuppliers };
}
