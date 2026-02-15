export interface Supplier {
    id: string;
    name: string;
    country: string;
    category: string;
    contact_email: string;
    website: string | null;
    is_active: boolean;
    created_at: string;
}

export interface CreateSupplierInput {
    name: string;
    country: string;
    category: string;
    contact_email: string;
    website?: string;
}
