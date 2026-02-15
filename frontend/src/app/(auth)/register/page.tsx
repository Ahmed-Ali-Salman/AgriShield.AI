'use client';
import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Input } from '@/components/ui/Input';
import { Button } from '@/components/ui/Button';
import { authService } from '@/services/authService';

export default function RegisterPage() {
  const [form, setForm] = useState({ email: '', password: '', full_name: '' });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const res = await authService.register(form);
      localStorage.setItem('access_token', res.data.access_token);
      document.cookie = `auth_token=${res.data.access_token}; path=/; max-age=${60 * 60 * 24 * 7}; SameSite=Lax`;
      router.push('/dashboard');
    } catch (e: any) {
      setError(e.response?.data?.detail || 'Registration failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className='auth-page'>
      <form className='auth-form' onSubmit={handleSubmit}>
        <h1>Create Account</h1>
        <Input label='Full Name' value={form.full_name} onChange={e => setForm({ ...form, full_name: e.target.value })} required />
        <Input label='Email' type='email' value={form.email} onChange={e => setForm({ ...form, email: e.target.value })} required />
        <Input label='Password' type='password' value={form.password} onChange={e => setForm({ ...form, password: e.target.value })} required />
        {error && <p style={{ color: 'var(--color-danger)', fontSize: '0.9rem' }}>{error}</p>}
        <Button type='submit' loading={loading}>Register</Button>
        <p style={{ textAlign: 'center', marginTop: '16px', color: 'var(--color-text-muted)', fontSize: '0.9rem' }}>
          Already have an account?{' '}
          <a href='/login' style={{ color: 'var(--color-primary)' }}>Sign in</a>
        </p>
      </form>
    </div>
  );
}
