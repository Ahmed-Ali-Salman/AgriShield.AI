'use client';
import React from 'react';
import { Sidebar } from '@/components/layout/Sidebar';
import { Header } from '@/components/layout/Header';
import { Providers } from '@/components/Providers';

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  return (
    <Providers>
      <div className='dashboard-layout'>
        <Sidebar />
        <div className='dashboard-content'>
          <Header />
          <main className='page-content'>{children}</main>
        </div>
      </div>
    </Providers>
  );
}
