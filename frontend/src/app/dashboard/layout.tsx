import React from 'react';
import { Sidebar } from '@/components/layout/Sidebar';
import { Header } from '@/components/layout/Header';

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className='dashboard-layout'>
      <Sidebar />
      <div className='dashboard-content'>
        <Header />
        <main className='page-content'>{children}</main>
      </div>
    </div>
  );
}
