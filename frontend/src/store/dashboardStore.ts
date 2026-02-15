import { create } from 'zustand';

interface DashboardState {
    totalSuppliers: number;
    openAlerts: number;
    setSummary: (total: number, alerts: number) => void;
}

export const useDashboardStore = create<DashboardState>((set) => ({
    totalSuppliers: 0,
    openAlerts: 0,
    setSummary: (total, alerts) => set({ totalSuppliers: total, openAlerts: alerts }),
}));
