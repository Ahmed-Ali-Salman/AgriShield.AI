'use client';
import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Input } from '@/components/ui/Input';
import { Button } from '@/components/ui/Button';
import { useAuth } from '@/hooks/useAuth';

export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const { login, loading, error } = useAuth();
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const result = await login({ email, password });
    if (result) router.push('/dashboard');
  };

  return (
    <div className='auth-page'>
      <form className='auth-form' onSubmit={handleSubmit}>
        <h1>AgriShield AI</h1>
        <p style={{ textAlign: 'center', color: 'var(--color-text-muted)', marginBottom: '24px', fontSize: '0.9rem' }}>
          Cyber-Resilient Food Supply Intelligence
        </p>
        <Input label='Email' type='email' value={email} onChange={e => setEmail(e.target.value)} required />
        <Input label='Password' type='password' value={password} onChange={e => setPassword(e.target.value)} required />
        {error && <p style={{ color: 'var(--color-danger)', fontSize: '0.9rem' }}>{error}</p>}
        <Button type='submit' loading={loading}>Sign In</Button>
        <p style={{ textAlign: 'center', marginTop: '16px', color: 'var(--color-text-muted)', fontSize: '0.9rem' }}>
          Don&apos;t have an account?{' '}
          <a href='/register' style={{ color: 'var(--color-primary)' }}>Create one</a>
        </p>
      </form>
    </div>
  );
}
