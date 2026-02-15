'use client';
import React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { LayoutDashboard, Users, ShieldAlert, Bell, Settings, LogOut } from 'lucide-react';
import { useAuth } from '@/hooks/useAuth';

const navItems = [
  { href: '/dashboard', label: 'Dashboard', icon: LayoutDashboard },
  { href: '/dashboard/suppliers', label: 'Suppliers', icon: Users },
  { href: '/dashboard/risk-scores', label: 'Risk Scores', icon: ShieldAlert },
  { href: '/dashboard/alerts', label: 'Alerts', icon: Bell },
  { href: '/dashboard/settings', label: 'Settings', icon: Settings },
];

export function Sidebar() {
  const pathname = usePathname();
  const { logout } = useAuth();

  return (
    <aside className='sidebar'>
      <div className='sidebar-brand'>
        <h2>AgriShield AI</h2>
      </div>
      <nav className='sidebar-nav'>
        {navItems.map(item => (
          <Link
            key={item.href}
            href={item.href}
            className={`sidebar-link ${pathname === item.href ? 'sidebar-link-active' : ''}`}
          >
            <item.icon size={20} />
            <span>{item.label}</span>
          </Link>
        ))}
      </nav>
      <div className='sidebar-footer'>
        <button onClick={logout} className='sidebar-link sidebar-logout'>
          <LogOut size={20} />
          <span>Logout</span>
        </button>
      </div>
    </aside>
  );
}
