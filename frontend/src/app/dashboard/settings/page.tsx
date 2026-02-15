'use client';
import React from 'react';
import { Card } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { useAuth } from '@/hooks/useAuth';

export default function SettingsPage() {
  const { logout } = useAuth();

  // Read user info from JWT token (decode payload)
  let userEmail = '';
  let userRole = '';
  if (typeof window !== 'undefined') {
    const token = localStorage.getItem('access_token');
    if (token) {
      try {
        const payload = JSON.parse(atob(token.split('.')[1]));
        userEmail = payload.sub || '';
        userRole = payload.role || '';
      } catch { /* ignore decode errors */ }
    }
  }

  return (
    <div>
      <h1 className='page-title'>Settings</h1>

      <Card title='Profile'>
        <div className='detail-meta' style={{ marginBottom: 16 }}>
          <div className='detail-meta-item'>
            <span className='detail-meta-label'>Email</span>
            <span className='detail-meta-value'>{userEmail || 'Unknown'}</span>
          </div>
          <div className='detail-meta-item'>
            <span className='detail-meta-label'>Role</span>
            <span className='detail-meta-value' style={{ textTransform: 'capitalize' }}>{userRole || 'Unknown'}</span>
          </div>
        </div>
      </Card>

      <Card title='Session' style={{ marginTop: 16 }}>
        <p style={{ color: 'var(--color-text-muted)', marginBottom: 16, fontSize: '0.9rem' }}>
          Sign out of your current session. You will need to log in again.
        </p>
        <Button variant='danger' onClick={logout}>
          Sign Out
        </Button>
      </Card>

      <Card title='About' style={{ marginTop: 16 }}>
        <p style={{ color: 'var(--color-text-muted)', fontSize: '0.9rem' }}>
          <strong>AgriShield AI</strong> v0.1.0<br />
          Cyber-Resilient Food Supply Intelligence Platform<br />
          &copy; 2026 All rights reserved.
        </p>
      </Card>
    </div>
  );
}
