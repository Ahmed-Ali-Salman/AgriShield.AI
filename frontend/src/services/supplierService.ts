import api from './api';
import { Supplier, CreateSupplierInput } from '@/types/supplier';

export const supplierService = {
    list: (skip = 0, limit = 20) =>
        api.get<Supplier[]>('/suppliers', { params: { skip, limit } }),
    getById: (id: string) =>
        api.get<Supplier>(`/suppliers/${id}`),
    create: (data: CreateSupplierInput) =>
        api.post<Supplier>('/suppliers', data),
    update: (id: string, data: Partial<CreateSupplierInput>) =>
        api.patch<Supplier>(`/suppliers/${id}`, data),
};
