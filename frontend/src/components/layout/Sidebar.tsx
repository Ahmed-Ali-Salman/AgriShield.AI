'use client';
import React from 'react';
import Link from 'next/link';
import { LayoutDashboard, Users, ShieldAlert, Bell, Settings, Upload } from 'lucide-react';

const navItems = [
  { href: '/dashboard', label: 'Dashboard', icon: LayoutDashboard },
  { href: '/dashboard/suppliers', label: 'Suppliers', icon: Users },
  { href: '/dashboard/risk-scores', label: 'Risk Scores', icon: ShieldAlert },
  { href: '/dashboard/alerts', label: 'Alerts', icon: Bell },
  { href: '/dashboard/settings', label: 'Settings', icon: Settings },
];

export function Sidebar() {
  return (
    <aside className='sidebar'>
      <div className='sidebar-brand'>
        <h2>AgriShield AI</h2>
      </div>
      <nav className='sidebar-nav'>
        {navItems.map(item => (
          <Link key={item.href} href={item.href} className='sidebar-link'>
            <item.icon size={20} />
            <span>{item.label}</span>
          </Link>
        ))}
      </nav>
    </aside>
  );
}
