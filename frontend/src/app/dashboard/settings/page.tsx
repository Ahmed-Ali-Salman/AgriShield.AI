import React from 'react';
import { Card } from '@/components/ui/Card';

export default function SettingsPage() {
  return (
    <div>
      <h1 className='page-title'>Settings</h1>
      <Card title='Account Settings'>
        <p>Profile, notification preferences, and API keys.</p>
      </Card>
    </div>
  );
}
